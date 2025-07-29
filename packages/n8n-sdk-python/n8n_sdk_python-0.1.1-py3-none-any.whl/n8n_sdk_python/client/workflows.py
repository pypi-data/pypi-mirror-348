"""
n8n Workflow API Client.
"""

from typing import Optional, Any

from ..client.base import BaseClient
from ..models.workflows import (
    Workflow, WorkflowList, WorkflowCreate, WorkflowUpdate, Tag, WorkflowTagUpdateRequestItem,
    Node, Connection, WorkflowSettings, WorkflowStaticData # WorkflowTransferPayload removed from imports
)
from ..models.base import N8nBaseModel # For generic responses
from ..utils.logger import log # Import logger


class WorkflowClient(BaseClient):
    """
    Client for interacting with n8n Workflow APIs.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def create_workflow(
        self,
        name: str,
        nodes: list[Node | dict[str, Any]],
        connections: dict[str, dict[str, list[Connection]]] | dict[str, Any], # Placeholder for now, complex conversion needed
        settings: Optional[WorkflowSettings | dict[str, Any]] = None,
        static_data: Optional[WorkflowStaticData | dict[str, int]] = None # Assuming WorkflowStaticData model
    ) -> Workflow:
        """
        Create a workflow in your instance.
        API Docs: https://docs.n8n.io/api/v1/workflows/#create-a-workflow
        """
        _nodes: list[Node] = []
        for node_input in nodes:
            if isinstance(node_input, dict):
                _nodes.append(Node(**node_input))
            elif isinstance(node_input, Node):
                _nodes.append(node_input)
            else:
                raise TypeError(f"Each item in 'nodes' must be a Node instance or a dict, got {type(node_input).__name__}")

        _settings: WorkflowSettings = WorkflowSettings()
        if settings is not None:
            if isinstance(settings, dict):
                _settings = WorkflowSettings(**settings)
            elif isinstance(settings, WorkflowSettings):
                _settings = settings
            else:
                raise TypeError(f"Parameter 'settings' must be a WorkflowSettings instance or a dict, got {type(settings).__name__}")

        _static_data: Optional[WorkflowStaticData] = None
        if static_data is not None:
            if isinstance(static_data, dict):
                _static_data = WorkflowStaticData(**static_data)
            elif isinstance(static_data, WorkflowStaticData):
                _static_data = static_data
            else:
                # Assuming str is not a valid type if model is WorkflowStaticData based on previous analysis
                raise TypeError(f"Parameter 'static_data' must be a WorkflowStaticData instance or a dict, got {type(static_data).__name__}")
        
        # TODO: Deep conversion for connections if it's a dict[str, Any]
        # For now, assuming if connections is dict[str, Any], it matches the structure Pydantic can parse
        # or it's already the correct ConnectionsDict type.
        # A proper conversion would iterate through the structure and convert Connection dicts.
        _connections = connections # Needs more robust handling if type is dict[str, Any]

        payload_model = WorkflowCreate(
            name=name,
            nodes=_nodes,
            connections=_connections, # type: ignore 
            settings=_settings,
            staticData=_static_data
        )
        payload = payload_model.model_dump(exclude_none=True)
        
        log.debug(f"Attempting to create workflow. Payload being sent: {payload}")

        response_data = await self.post(endpoint="/v1/workflows", json=payload)
        return Workflow(**response_data)

    async def list_workflows(
        self,
        active: Optional[bool] = None,
        tags: Optional[str] = None, # Comma-separated string of tag names
        name: Optional[str] = None,
        project_id: Optional[str] = None,
        exclude_pinned_data: Optional[bool] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None
    ) -> WorkflowList:
        """
        Retrieve all workflows from your instance.
        API Docs: https://docs.n8n.io/api/v1/workflows/#retrieve-all-workflows
        """
        params: dict[str, Any] = {}
        if active is not None:
            params["active"] = active
        if tags is not None:
            params["tags"] = tags
        if name is not None:
            params["name"] = name
        if project_id is not None:
            params["projectId"] = project_id
        if exclude_pinned_data is not None:
            params["excludePinnedData"] = exclude_pinned_data
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor
        
        response_data = await self.get(endpoint="/v1/workflows", params=params)
        return WorkflowList(**response_data)

    async def get_workflow(
        self,
        workflow_id: str,
        exclude_pinned_data: Optional[bool] = None
    ) -> Workflow:
        """
        Retrieves a workflow.
        API Docs: https://docs.n8n.io/api/v1/workflows/#retrieves-a-workflow
        """
        params: dict[str, Any] = {}
        if exclude_pinned_data is not None:
            params["excludePinnedData"] = exclude_pinned_data
            
        response_data = await self.get(endpoint=f"/v1/workflows/{workflow_id}", params=params)
        return Workflow(**response_data)

    async def delete_workflow(
        self,
        workflow_id: str
    ) -> Workflow: # API doc states it returns the deleted workflow object
        """
        Deletes a workflow.
        API Docs: https://docs.n8n.io/api/v1/workflows/#delete-a-workflow
        """
        response_data = await self.delete(endpoint=f"/v1/workflows/{workflow_id}")
        return Workflow(**response_data)

    async def update_workflow(
        self,
        workflow_id: str,
        name: str, 
        nodes: list[Node | dict[str, Any]],
        connections: dict[str, dict[str, list[Connection]]] | dict[str, Any], # Placeholder for now
        settings: WorkflowSettings | dict[str, Any],
        static_data: Optional[WorkflowStaticData | dict[str, Any]] = None # Assuming WorkflowStaticData
    ) -> Workflow:
        """
        Update a workflow.
        API Docs: https://docs.n8n.io/api/v1/workflows/#update-a-workflow
        """
        processed_nodes: list[Node] = []
        if nodes:
            for node_input in nodes:
                if isinstance(node_input, dict):
                    processed_nodes.append(Node(**node_input))
                elif isinstance(node_input, Node):
                    processed_nodes.append(node_input)
                else:
                    raise TypeError(f"Each item in 'nodes' must be a Node instance or a dict, got {type(node_input).__name__}")

        processed_settings: WorkflowSettings
        if isinstance(settings, dict):
            processed_settings = WorkflowSettings(**settings)
        elif isinstance(settings, WorkflowSettings):
            processed_settings = settings
        else:
            raise TypeError(f"Parameter 'settings' must be a WorkflowSettings instance or a dict, got {type(settings).__name__}")

        processed_static_data: Optional[WorkflowStaticData] = None
        if static_data is not None:
            if isinstance(static_data, dict):
                processed_static_data = WorkflowStaticData(**static_data)
            elif isinstance(static_data, WorkflowStaticData):
                processed_static_data = static_data
            else:
                raise TypeError(f"Parameter 'static_data' must be a WorkflowStaticData instance or a dict, got {type(static_data).__name__}")

        # TODO: Deep conversion for connections
        processed_connections = connections # Needs robust handling

        update_payload_model = WorkflowUpdate(
            name=name, 
            nodes=processed_nodes, 
            connections=processed_connections, # type: ignore
            settings=processed_settings,
            staticData=processed_static_data
        )
        update_payload = update_payload_model.model_dump(exclude_none=True)
        
        response_data = await self.put(endpoint=f"/v1/workflows/{workflow_id}", json=update_payload)
        return Workflow(**response_data)

    async def activate_workflow(
        self,
        workflow_id: str
    ) -> Workflow:
        """
        Activate a workflow.
        API Docs: https://docs.n8n.io/api/v1/workflows/#activate-a-workflow
        """
        response_data = await self.post(endpoint=f"/v1/workflows/{workflow_id}/activate")
        return Workflow(**response_data)

    async def deactivate_workflow(
        self,
        workflow_id: str
    ) -> Workflow:
        """
        Deactivate a workflow.
        API Docs: https://docs.n8n.io/api/v1/workflows/#deactivate-a-workflow
        """
        response_data = await self.post(endpoint=f"/v1/workflows/{workflow_id}/deactivate")
        return Workflow(**response_data)

    async def transfer_workflow_to_project(
        self,
        workflow_id: str,
        destination_project_id: str # Parameter type simplified to str
    ) -> N8nBaseModel: # API returns 200, docs don't specify body. Assuming generic success.
        """
        Transfer a workflow to another project.
        API Docs: https://docs.n8n.io/api/v1/workflows/#transfer-a-workflow-to-another-project
        """
        _payload = {"destinationProjectId": destination_project_id} # Direct payload construction
        response_data = await self.put(endpoint=f"/v1/workflows/{workflow_id}/transfer", json=_payload)
        return N8nBaseModel()

    async def get_workflow_tags(
        self,
        workflow_id: str
    ) -> list[Tag]:
        """
        Get workflow tags.
        API Docs: https://docs.n8n.io/api/v1/workflows/#get-workflow-tags
        """
        response_data = await self.get(endpoint=f"/v1/workflows/{workflow_id}/tags")
        return [Tag(**tag_data) for tag_data in response_data]

    async def update_workflow_tags(
        self,
        workflow_id: str,
        tags: list[WorkflowTagUpdateRequestItem | dict[str, Any]] 
    ) -> list[Tag]:
        """
        Update tags of a workflow.
        API Docs: https://docs.n8n.io/api/v1/workflows/#update-tags-of-a-workflow
        """
        processed_tags: list[WorkflowTagUpdateRequestItem] = []
        if tags:
            for tag_input in tags:
                if isinstance(tag_input, dict):
                    processed_tags.append(WorkflowTagUpdateRequestItem(**tag_input))
                elif isinstance(tag_input, WorkflowTagUpdateRequestItem):
                    processed_tags.append(tag_input)
                else:
                    raise TypeError(f"Each item in 'tags' must be a WorkflowTagUpdateRequestItem instance or a dict, got {type(tag_input).__name__}")
        
        payload = [tag_item.model_dump() for tag_item in processed_tags]
        response_data = await self.put(endpoint=f"/v1/workflows/{workflow_id}/tags", json=payload)
        return [Tag(**tag_data) for tag_data in response_data] 