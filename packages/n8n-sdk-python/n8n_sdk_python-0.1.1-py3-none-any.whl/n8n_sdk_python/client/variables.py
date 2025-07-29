"""
n8n Variables API Client.
"""

from typing import Optional, Any

from ..client.base import BaseClient
from ..models.variables import Variable, VariablesList, VariableCreate
from ..models.base import N8nBaseModel # For generic 204 response


class VariableClient(BaseClient):
    """
    Client for interacting with n8n Variables APIs.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def create_variable(
        self,
        key: str,
        value: str # Model VariableCreate specifies value as str
    ) -> Variable: # Tools-API.md suggests Variable or operation status. N8N-API.md says 201, implies returning created object.
        """
        Create a variable in your instance.
        API Docs: https://docs.n8n.io/api/v1/variables/#create-a-variable
        """
        payload = VariableCreate(key=key, value=value).model_dump()
        response_data = await self.post(endpoint="/v1/variables", json=payload)
        # N8N-API.md doesn't show response body for 201, but typically created object is returned.
        # Assuming response_data is the created Variable object based on common REST patterns.
        return Variable(**response_data) 

    async def list_variables(
        self,
        limit: Optional[int] = None,
        cursor: Optional[str] = None
    ) -> VariablesList:
        """
        Retrieve variables from your instance.
        API Docs: https://docs.n8n.io/api/v1/variables/#retrieve-variables
        """
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor
        
        response_data = await self.get(endpoint="/v1/variables", params=params)
        return VariablesList(**response_data)

    async def delete_variable(
        self,
        variable_id: str
    ) -> None: # API returns 204 No Content
        """
        Delete a variable from your instance.
        API Docs: https://docs.n8n.io/api/v1/variables/#delete-a-variable
        """
        await self.delete(endpoint=f"/v1/variables/{variable_id}")
        return None 