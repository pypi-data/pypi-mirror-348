"""
n8n SourceControl API Client.
"""

from typing import Optional, Any

from ..client.base import BaseClient
from ..models.source_control import ScmPullResponse, ScmPullRequest


class SourceControlClient(BaseClient):
    """
    Client for interacting with n8n SourceControl APIs.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def pull_from_source_control(
        self,
        force: Optional[bool] = None,
        variables: Optional[dict[str, Any]] = None
    ) -> ScmPullResponse:
        """
        Pull changes from the remote repository.
        Requires the Source Control feature to be licensed and connected to a repository.
        API Docs: https://docs.n8n.io/api/v1/source-control/#pull-changes-from-the-remote-repository
        """
        payload = ScmPullRequest(force=force, variables=variables).model_dump(exclude_none=True)
        
        response_data = await self.post(endpoint="/v1/source-control/pull", json=payload)
        return ScmPullResponse(**response_data) 