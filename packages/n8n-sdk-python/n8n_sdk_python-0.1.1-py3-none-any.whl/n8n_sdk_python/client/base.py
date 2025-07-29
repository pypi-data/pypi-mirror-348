import os
from typing import Any, Optional

import httpx

from ..utils.logger import log
from ..utils.errors import N8nAPIError


class BaseClient:
    """n8n API 客戶端基礎類，提供基本的 HTTP 方法"""
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None, timeout: int = 30):
        """
        初始化 n8n API 客戶端
        
        Args:
            base_url: n8n API 的基礎 URL，默認使用配置中的值
            api_key: n8n API 金鑰，默認使用配置中的值
        """
        self.base_url = base_url or os.getenv("N8N_BASE_URL", "http://localhost:5678")
        self.api_key = api_key or os.getenv("N8N_API_KEY")
        self.headers = {"X-N8N-API-KEY": self.api_key} if self.api_key else {}
        self.timeout = timeout
    
    async def _request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[dict[str, Any]] = None,
        json_payload: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
        timeout: Optional[int] = None
    ) -> Any:
        """
        執行 HTTP 請求
        
        Args:
            method: HTTP 方法 (GET, POST, PATCH, DELETE)
            endpoint: API 端點路徑
            params: URL 查詢參數
            json_payload: 請求體 JSON 資料
            headers: 額外的 HTTP 標頭
            timeout: 請求超時時間（秒）
            
        Returns:
            響應資料（通常是字典或列表）
            
        Raises:
            N8nApiError: 當 API 請求失敗時
        """
        url = f"{self.base_url}/api/{endpoint.lstrip('/')}"
        request_headers = {**self.headers, **(headers or {})}
        
        log.debug(f"Requesting {method} {url} with payload: {json_payload}")
        
        try:
            async with httpx.AsyncClient() as client:
                request_kwargs = {
                    "method": method,
                    "url": url,
                    "params": params,
                    "headers": request_headers,
                    "timeout": timeout or self.timeout
                }
                if json_payload is not None:
                    request_kwargs["json"] = json_payload
                elif method in ["POST", "PUT", "PATCH"]:
                    request_kwargs["content"] = b''
                
                response = await client.request(**request_kwargs)
                
                log.debug(f"Response status: {response.status_code}")
                
                # 嘗試以 JSON 解析響應
                if response.content:
                    try:
                        response_data = response.json()
                    except ValueError:
                        response_data = response.text
                else:
                    response_data = None
                
                # 檢查錯誤
                if response.is_error:
                    error_msg = f"n8n API error: {response.status_code}"
                    if isinstance(response_data, dict) and "message" in response_data:
                        error_msg = f"{error_msg} - {response_data['message']}"
                    
                    raise N8nAPIError(
                        message=error_msg,
                        status_code=response.status_code,
                        response_body=response.text,
                        details={"endpoint": endpoint, "method": method}
                    )
                
                return response_data
                
        except httpx.RequestError as e:
            error_msg = f"Request error: {str(e)}"
            log.error(error_msg)
            raise N8nAPIError(
                message=error_msg,
                details={"endpoint": endpoint, "method": method}
            )
    
    async def get(
        self, 
        endpoint: str, 
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None
    ) -> Any:
        """執行 GET 請求"""
        return await self._request("GET", endpoint, params=params, headers=headers)
    
    async def put(
        self,
        endpoint: str,
        json: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None
    ) -> Any:
        """執行 PUT 請求"""
        return await self._request("PUT", endpoint, json_payload=json, params=params, headers=headers)
    
    async def post(
        self, 
        endpoint: str, 
        json: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None
    ) -> Any:
        """執行 POST 請求"""
        return await self._request("POST", endpoint, json_payload=json, params=params, headers=headers)
    
    async def patch(
        self, 
        endpoint: str, 
        json: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None
    ) -> Any:
        """執行 PATCH 請求"""
        return await self._request("PATCH", endpoint, json_payload=json, params=params, headers=headers)
    
    async def delete(
        self, 
        endpoint: str, 
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None
    ) -> Any:
        """執行 DELETE 請求"""
        return await self._request("DELETE", endpoint, params=params, headers=headers) 