"""
n8n Projects API Client.
"""

from typing import Optional, Any

from ..client.base import BaseClient
from ..models.projects import Project, ProjectList, ProjectCreate, ProjectUpdate # ProjectUpdate is also needed
from ..models.base import N8nBaseModel # For generic 204 response


class ProjectClient(BaseClient):
    """
    Client for interacting with n8n Projects APIs.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def create_project(
        self,
        name: str
    ) -> Project: # Tools-API.md suggests Project or operation status. N8N-API.md says 201, implies returning created object.
        """
        Create a project in your instance.
        API Docs: https://docs.n8n.io/api/v1/projects/#create-a-project
        """
        payload = ProjectCreate(name=name).model_dump()
        response_data = await self.post(endpoint="/v1/projects", json=payload)
        # N8N-API.md doesn't show response body for 201, but typically created object is returned.
        return Project(**response_data)

    async def list_projects(
        self,
        limit: Optional[int] = None,
        cursor: Optional[str] = None
    ) -> ProjectList:
        """
        Retrieve projects from your instance.
        API Docs: https://docs.n8n.io/api/v1/projects/#retrieve-projects
        """
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor
        
        response_data = await self.get(endpoint="/v1/projects", params=params)
        return ProjectList(**response_data)

    async def delete_project(
        self,
        project_id: str
    ) -> None: # API returns 204 No Content
        """
        Delete a project from your instance.
        API Docs: https://docs.n8n.io/api/v1/projects/#delete-a-project
        """
        await self.delete(endpoint=f"/v1/projects/{project_id}")
        return None

    async def update_project(
        self,
        project_id: str,
        name: str
    ) -> None: # API returns 204 No Content
        """
        Update a project.
        API Docs: https://docs.n8n.io/api/v1/projects/#update-a-project (N8N-API.md has this under /project/put...)
                                                                      (Tools-API.md path is PUT /projects/{projectId})
        """
        payload = ProjectUpdate(name=name).model_dump()
        await self.put(endpoint=f"/v1/projects/{project_id}", json=payload)
        return None 