"""
n8n Execution API Client.
"""

from typing import Optional, Any

from ..client.base import BaseClient
from ..models.executions import (
    ExecutionList, Execution, ExecutionStatus
)


class ExecutionClient(BaseClient):
    """
    Client for interacting with n8n Execution APIs.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def list_executions(
        self,
        include_data: Optional[bool] = None,
        status: Optional[ExecutionStatus] = None, # Use ExecutionStatus enum from models
        workflow_id: Optional[str] = None,
        project_id: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None
    ) -> ExecutionList:
        """
        Retrieve all executions from your instance.
        API Docs: https://docs.n8n.io/api/v1/executions/#retrieve-all-executions
        """
        params: dict[str, Any] = {}
        if include_data is not None:
            params["includeData"] = include_data
        if status is not None:
            params["status"] = status.value # Get the string value from enum
        if workflow_id is not None:
            params["workflowId"] = workflow_id
        if project_id is not None:
            params["projectId"] = project_id
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor
        
        response_data = await self.get(endpoint="/v1/executions", params=params)
        return ExecutionList(**response_data)

    async def get_execution(
        self,
        execution_id: int | str, # Changed Union to |
        include_data: Optional[bool] = None
    ) -> Execution:
        """
        Retrieve an execution from your instance.
        API Docs: https://docs.n8n.io/api/v1/executions/#retrieve-an-execution
        """
        params: dict[str, Any] = {}
        if include_data is not None:
            params["includeData"] = include_data
            
        response_data = await self.get(endpoint=f"/v1/executions/{execution_id}", params=params)
        return Execution(**response_data)

    async def delete_execution(
        self,
        execution_id: int | str 
    ) -> Execution: # API doc states it returns the deleted execution object
        """
        Deletes an execution from your instance.
        API Docs: https://docs.n8n.io/api/v1/executions/#delete-an-execution
        """
        response_data = await self.delete(endpoint=f"/v1/executions/{execution_id}")
        return Execution(**response_data) 