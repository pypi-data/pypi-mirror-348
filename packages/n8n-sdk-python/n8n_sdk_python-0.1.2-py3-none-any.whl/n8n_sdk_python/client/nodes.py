"""
n8n 節點 API 客戶端。
處理節點類型的獲取和節點操作。
"""

from typing import Any, Optional

from pydantic import ValidationError

from ..client.base import BaseClient
from ..utils.logger import log
from ..models.nodes import (
    NodeType,
    NodeTypeDescription,
    NodeParameterOptions,
    NodeConnectionOptions
)


class NodesClient(BaseClient):
    """n8n 節點 API 客戶端類"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def get_node_types(self) -> list[NodeType]:
        """
        獲取所有可用的節點類型
        
        Returns:
            節點類型列表
        """
        try:
            response = await self.get("/node-types")
            
            node_types = []
            for item in response.get("data", []):
                try:
                    node_types.append(NodeType(**item))
                except ValidationError:
                    pass  # 忽略無效的節點類型數據
            
            return node_types
        except Exception as e:
            log.error(f"獲取節點類型列表失敗: {str(e)}")
            return []
    
    async def get_node_type(self, type_name: str) -> Optional[NodeTypeDescription]:
        """
        獲取特定節點類型的詳細信息
        
        Args:
            type_name: 節點類型名稱，例如 'n8n-nodes-base.httpRequest'
            
        Returns:
            節點類型描述，如果找不到則返回 None
        """
        try:
            response = await self.get(f"/node-types/{type_name}")
            
            if not response or "data" not in response:
                return None
                
            return NodeTypeDescription(**response["data"])
        except Exception as e:
            log.error(f"獲取節點類型 {type_name} 失敗: {str(e)}")
            return None
    
    async def get_parameter_options(
        self, 
        type_name: str,
        method_name: str,
        path: str,
        payload: Optional[dict[str, Any]] = None
    ) -> Optional[NodeParameterOptions]:
        """
        獲取節點參數的可選值
        
        Args:
            type_name: 節點類型名稱
            method_name: 請求方法名稱
            path: 參數路徑 (例如: 'parameters.resource')
            payload: 請求的附加數據
            
        Returns:
            參數選項，如果找不到則返回 None
        """
        try:
            request_data = {
                "nodeTypeAndVersion": type_name,
                "methodName": method_name,
                "path": path,
                **(payload or {})
            }
            
            response = await self.post(
                "/node-parameter-options", 
                json=request_data
            )
            
            if not response or "data" not in response:
                return None
                
            return NodeParameterOptions(**response["data"])
        except Exception as e:
            log.error(f"獲取節點 {type_name} 參數選項失敗: {str(e)}")
            return None
    
    async def get_connection_options(
        self, 
        node_type: str,
        connections_options: dict[str, Any],
        node_filter: Optional[dict[str, Any]] = None
    ) -> Optional[NodeConnectionOptions]:
        """
        獲取節點連接的可選值
        
        Args:
            node_type: 節點類型名稱
            connections_options: 連接選項配置
            node_filter: 節點過濾條件
            
        Returns:
            連接選項，如果獲取失敗則返回 None
        """
        try:
            request_data = {
                "nodeType": node_type,
                "connectionsOptions": connections_options,
                **({"nodeFilter": node_filter} if node_filter else {})
            }
            
            response = await self.post(
                "/node-connection-options", 
                json=request_data
            )
            
            if not response or "data" not in response:
                return None
                
            return NodeConnectionOptions(**response["data"])
        except Exception as e:
            log.error(f"獲取節點連接選項失敗: {str(e)}")
            return None 