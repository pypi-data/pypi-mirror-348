"""
n8n Credential API Client.
"""

from typing import Any, Optional
from pydantic import ValidationError

from ..client.base import BaseClient
from ..models.credentials import (
    CredentialListItem,
    CredentialDetail,
    CredentialTestResult,
    CredentialTypeDescription,
    CredentialTypeList,
    CredentialShort,
    CredentialDataSchemaResponse,
    CredentialCreate
)
from ..models.base import N8nBaseModel
from ..utils.logger import log


class CredentialClient(BaseClient):
    """
    Client for interacting with n8n Credential APIs.
    """
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        初始化憑證客戶端
        
        Args:
            base_url: n8n API 的基礎 URL
            api_key: n8n API 金鑰
        """
        super().__init__(base_url=base_url, api_key=api_key)
        self._credential_types_cache = None
    
    async def get_credentials(self, credential_type: Optional[str] = None) -> list[CredentialListItem]:
        """
        獲取憑證列表
        
        Args:
            credential_type: 按憑證類型過濾
            
        Returns:
            憑證列表
        """
        params: dict[str, Any] = {}
        if credential_type:
            params["type"] = credential_type
        
        try:
            response = await self.get("/v1/credentials", params=params)
            credentials = []
            for item in response.get("data", []):
                credentials.append(CredentialListItem(**item))
            return credentials
        except Exception as e:
            log.error(f"獲取憑證列表失敗: {str(e)}")
            return []
    
    async def get_credential(self, credential_id: str) -> Optional[CredentialDetail]:
        """
        獲取指定 ID 的憑證詳情
        
        Args:
            credential_id: 憑證 ID
            
        Returns:
            憑證詳情，如果不存在則返回 None
        """
        try:
            response = await self.get(f"/v1/credentials/{credential_id}")
            if response:
                return CredentialDetail(**response)
            return None
        except Exception as e:
            log.error(f"獲取憑證 {credential_id} 失敗: {str(e)}")
            return None
    
    async def create_credential(
        self,
        name: str,
        credential_type: str,
        data: dict[str, Any]
    ) -> CredentialShort:
        """
        Creates a credential.
        API Docs: https://docs.n8n.io/api/v1/credentials/#create-a-credential
        """
        payload = CredentialCreate(name=name, type=credential_type, data=data).model_dump()
        response_data = await self.post(endpoint="/v1/credentials", json=payload)
        return CredentialShort(**response_data)
    
    async def update_credential(self, credential_id: str, credential_data: dict[str, Any]) -> Optional[CredentialDetail]:
        """
        更新指定 ID 的憑證
        
        Args:
            credential_id: 憑證 ID
            credential_data: 憑證數據
            
        Returns:
            更新後的憑證，如果失敗則返回 None
        """
        try:
            response = await self.patch(f"/v1/credentials/{credential_id}", json=credential_data)
            if response:
                return CredentialDetail(**response)
            return None
        except Exception as e:
            log.error(f"更新憑證 {credential_id} 失敗: {str(e)}")
            return None
    
    async def delete_credential(
        self,
        credential_id: str
    ) -> CredentialShort:
        """
        Deletes a credential from your instance.
        API Docs: https://docs.n8n.io/api/v1/credentials/#delete-credential-by-id
        """
        response_data = await self.delete(endpoint=f"/v1/credentials/{credential_id}")
        return CredentialShort(**response_data)
    
    async def test_credential(self, credential_id: str) -> Optional[CredentialTestResult]:
        """
        測試憑證是否有效
        
        Args:
            credential_id: 憑證 ID
            
        Returns:
            測試結果，如果失敗則返回 None
        """
        try:
            response = await self.post(f"/v1/credentials/{credential_id}/test")
            if response:
                return CredentialTestResult(
                    status="success" if response.get("status", "").lower() != "error" else "error",
                    message=response.get("message")
                )
            return None
        except Exception as e:
            log.error(f"測試憑證 {credential_id} 失敗: {str(e)}")
            return CredentialTestResult(status="error", message=str(e))
    
    async def get_credential_types(self, use_cache: bool = True) -> dict[str, CredentialTypeDescription]:
        """
        獲取所有可用的憑證類型
        
        Args:
            use_cache: 是否使用緩存，如果為 True 且已有緩存則返回緩存結果
            
        Returns:
            憑證類型字典
        """
        if use_cache and self._credential_types_cache is not None:
            return self._credential_types_cache
        
        try:
            response = await self.get("/v1/credentials/types")
            credential_types = {}
            
            for type_name, type_data in response.items():
                credential_types[type_name] = CredentialTypeDescription(
                    name=type_name,
                    displayName=type_data.get("displayName", type_name),
                    properties=type_data.get("properties", []),
                    authenticate=type_data.get("authenticate")
                )
            
            self._credential_types_cache = credential_types
            return credential_types
        except Exception as e:
            log.error(f"獲取憑證類型列表失敗: {str(e)}")
            return {}
    
    async def get_credential_type(self, type_name: str) -> Optional[CredentialTypeDescription]:
        """
        獲取指定名稱的憑證類型
        
        Args:
            type_name: 憑證類型名稱
            
        Returns:
            憑證類型詳情，如果不存在則返回 None
        """
        types = await self.get_credential_types()
        return types.get(type_name)

    async def get_credential_schema(
        self,
        credential_type_name: str
    ) -> CredentialDataSchemaResponse:
        """
        Show credential data schema.
        API Docs: https://docs.n8n.io/api/v1/credentials/#show-credential-data-schema
        """
        response_data = await self.get(endpoint=f"/v1/credentials/schema/{credential_type_name}")
        if isinstance(response_data, dict):
            return CredentialDataSchemaResponse(**response_data)
        raise ValueError("Unexpected response format for credential schema")

    async def transfer_credential_to_project(
        self,
        credential_id: str,
        destination_project_id: str
    ) -> N8nBaseModel:
        """
        Transfer a credential to another project.
        API Docs: https://docs.n8n.io/api/v1/credentials/#transfer-a-credential-to-another-project
                  (Note: API docs link this under Workflow section, but path is /credentials/.../transfer)
        """
        _payload = {"destinationProjectId": destination_project_id}
        response_data = await self.put(endpoint=f"/v1/credentials/{credential_id}/transfer", json=_payload)
        return N8nBaseModel() 