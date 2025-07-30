"""
Shopify GraphQL API Client
Based on PR #9 architecture with PR #20 error handling and PR #25 network resilience
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
from urllib.parse import urljoin
import backoff
import httpx
from functools import lru_cache

logger = logging.getLogger(__name__)


class ShopifyGraphQLError(Exception):
    """GraphQL特有のエラー（PR #20のアプローチを採用）"""
    
    def __init__(self, message: str, errors: Optional[List[Dict]] = None, response: Optional[httpx.Response] = None):
        super().__init__(message)
        self.errors = errors or []
        self.response = response
        self.query_cost = None
        
        # GraphQL特有のエラー情報を解析
        if errors:
            for error in errors:
                extensions = error.get('extensions', {})
                if 'cost' in extensions:
                    self.query_cost = extensions['cost']


class ShopifyGraphQLAPI:
    """
    GraphQL API client for Shopify
    PR #9をベースに、PR #7の後方互換性とPR #20のエラーハンドリングを統合
    """
    
    def __init__(self, shop_url: str, access_token: str, api_version: str = "2025-04"):
        self.shop_url = shop_url.strip('/')
        self.access_token = access_token
        self.api_version = api_version
        self.endpoint = f"{self.shop_url}/admin/api/{api_version}/graphql.json"
        
        # PR #25のネットワーク耐性機能との統合
        self.retry_config = {
            'max_retries': int(os.getenv('INSTALL_RETRY', '3')),
            'timeout': int(os.getenv('INSTALL_TIMEOUT', '120')),
            'backoff_factor': 2,
        }
        
        # HTTP client configuration
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(self.retry_config['timeout']),
            headers={
                'X-Shopify-Access-Token': self.access_token,
                'Content-Type': 'application/json',
            }
        )
        
        # Query cost tracking for rate limiting
        self.cost_limit = 1000
        self.cost_available = 1000
        self.cost_restore_rate = 50
        
    @backoff.on_exception(
        backoff.expo,
        (httpx.RequestError, httpx.TimeoutException),
        max_tries=lambda self: self.retry_config['max_retries'],
        max_time=lambda self: self.retry_config['timeout']
    )
    async def execute_query(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        GraphQLクエリを実行し、結果を返す
        PR #25のネットワーク耐性機能を活用
        """
        payload = {
            'query': query,
            'variables': variables or {}
        }
        
        try:
            response = await self.client.post(
                self.endpoint,
                json=payload
            )
            
            # レート制限情報を更新
            self._update_rate_limit_info(response.headers)
            
            response_data = response.json()
            
            # GraphQLエラーをチェック
            if 'errors' in response_data:
                raise ShopifyGraphQLError(
                    "GraphQL query failed",
                    errors=response_data['errors'],
                    response=response
                )
            
            return response_data.get('data', {})
            
        except httpx.RequestError as e:
            logger.error(f"Network error during GraphQL request: {e}")
            raise ShopifyGraphQLError(f"Network error: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse GraphQL response: {e}")
            raise ShopifyGraphQLError(f"Invalid response format: {e}")
    
    def _update_rate_limit_info(self, headers: Dict[str, str]):
        """レート制限情報を更新"""
        if 'X-Shopify-API-Call-Limit' in headers:
            parts = headers['X-Shopify-API-Call-Limit'].split('/')
            if len(parts) == 2:
                self.cost_available = int(parts[1]) - int(parts[0])
                self.cost_limit = int(parts[1])
    
    @lru_cache(maxsize=128)
    def _build_query_fragment(self, entity_type: str, fields: List[str]) -> str:
        """
        指定されたエンティティタイプとフィールドに基づいてGraphQLフラグメントを構築
        キャッシュにより同じクエリの再構築を防ぐ
        """
        if entity_type == "Order":
            return self._build_order_fragment(fields)
        elif entity_type == "Product":
            return self._build_product_fragment(fields)
        elif entity_type == "Customer":
            return self._build_customer_fragment(fields)
        else:
            raise ValueError(f"Unsupported entity type: {entity_type}")
    
    def _build_order_fragment(self, fields: List[str]) -> str:
        """Order用のGraphQLフラグメントを構築"""
        base_fields = ['id', 'name', 'totalPrice', 'createdAt']
        
        # デフォルトのフィールドと要求されたフィールドをマージ
        all_fields = list(set(base_fields + fields))
        
        fragment = "fragment OrderFields on Order {\n"
        
        for field in all_fields:
            if field == 'lineItems':
                fragment += """
                    lineItems(first: 50) {
                        edges {
                            node {
                                id
                                title
                                quantity
                                price
                                product {
                                    id
                                    title
                                }
                            }
                        }
                        pageInfo {
                            hasNextPage
                            endCursor
                        }
                    }
                """
            elif field == 'customer':
                fragment += """
                    customer {
                        id
                        displayName
                        email
                    }
                """
            else:
                fragment += f"    {field}\n"
        
        fragment += "}"
        return fragment
    
    def _build_product_fragment(self, fields: List[str]) -> str:
        """Product用のGraphQLフラグメントを構築"""
        base_fields = ['id', 'title', 'handle', 'createdAt']
        all_fields = list(set(base_fields + fields))
        
        fragment = "fragment ProductFields on Product {\n"
        
        for field in all_fields:
            if field == 'variants':
                fragment += """
                    variants(first: 50) {
                        edges {
                            node {
                                id
                                title
                                price
                                availableForSale
                                inventoryQuantity
                            }
                        }
                        pageInfo {
                            hasNextPage
                            endCursor
                        }
                    }
                """
            elif field == 'images':
                fragment += """
                    images(first: 10) {
                        edges {
                            node {
                                id
                                url
                                altText
                            }
                        }
                    }
                """
            else:
                fragment += f"    {field}\n"
        
        fragment += "}"
        return fragment
    
    def _build_customer_fragment(self, fields: List[str]) -> str:
        """Customer用のGraphQLフラグメントを構築"""
        base_fields = ['id', 'displayName', 'email', 'createdAt']
        all_fields = list(set(base_fields + fields))
        
        fragment = "fragment CustomerFields on Customer {\n"
        
        for field in all_fields:
            if field == 'addresses':
                fragment += """
                    addresses(first: 10) {
                        edges {
                            node {
                                id
                                address1
                                city
                                province
                                country
                            }
                        }
                    }
                """
            elif field == 'orders':
                fragment += """
                    orders(first: 10) {
                        edges {
                            node {
                                id
                                name
                                totalPrice
                                createdAt
                            }
                        }
                        pageInfo {
                            hasNextPage
                            endCursor
                        }
                    }
                """
            else:
                fragment += f"    {field}\n"
        
        fragment += "}"
        return fragment
    
    # 基本的なクエリメソッド
    async def get_orders(self, first: int = 50, after: Optional[str] = None,
                        status: Optional[str] = None, created_at_min: Optional[str] = None,
                        created_at_max: Optional[str] = None, fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        注文情報を取得するGraphQLクエリ
        PR #7の機能を参考に実装
        """
        fields = fields or ['lineItems', 'customer', 'totalPrice', 'currencyCode']
        fragment = self._build_query_fragment('Order', fields)
        
        query = f"""
        {fragment}
        
        query GetOrders($first: Int!, $after: String, $query: String) {{
            orders(first: $first, after: $after, query: $query) {{
                edges {{
                    node {{
                        ...OrderFields
                    }}
                }}
                pageInfo {{
                    hasNextPage
                    endCursor
                }}
            }}
        }}
        """
        
        # Build query string for filtering
        query_parts = []
        if status:
            query_parts.append(f"status:{status}")
        if created_at_min:
            query_parts.append(f"created_at:>={created_at_min}")
        if created_at_max:
            query_parts.append(f"created_at:<={created_at_max}")
        
        variables = {
            'first': first,
            'after': after,
            'query': ' AND '.join(query_parts) if query_parts else None
        }
        
        return await self.execute_query(query, variables)
    
    async def get_products(self, first: int = 50, after: Optional[str] = None,
                          fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        商品情報を取得するGraphQLクエリ
        """
        fields = fields or ['variants', 'images', 'status', 'vendor']
        fragment = self._build_query_fragment('Product', fields)
        
        query = f"""
        {fragment}
        
        query GetProducts($first: Int!, $after: String) {{
            products(first: $first, after: $after) {{
                edges {{
                    node {{
                        ...ProductFields
                    }}
                }}
                pageInfo {{
                    hasNextPage
                    endCursor
                }}
            }}
        }}
        """
        
        variables = {
            'first': first,
            'after': after
        }
        
        return await self.execute_query(query, variables)
    
    async def get_customers(self, first: int = 50, after: Optional[str] = None,
                           fields: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        顧客情報を取得するGraphQLクエリ
        """
        fields = fields or ['addresses', 'orders', 'tags']
        fragment = self._build_query_fragment('Customer', fields)
        
        query = f"""
        {fragment}
        
        query GetCustomers($first: Int!, $after: String) {{
            customers(first: $first, after: $after) {{
                edges {{
                    node {{
                        ...CustomerFields
                    }}
                }}
                pageInfo {{
                    hasNextPage
                    endCursor
                }}
            }}
        }}
        """
        
        variables = {
            'first': first,
            'after': after
        }
        
        return await self.execute_query(query, variables)
    
    async def close(self):
        """クライアントを閉じる"""
        await self.client.aclose()
    
    # Context manager support
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


# Import for backward compatibility
import os