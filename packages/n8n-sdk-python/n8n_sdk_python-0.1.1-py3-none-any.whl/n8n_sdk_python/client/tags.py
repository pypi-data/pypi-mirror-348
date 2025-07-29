"""
n8n Tags API Client.
"""

from typing import Optional, Any

from ..client.base import BaseClient
from ..models.workflows import Tag, TagList


class TagClient(BaseClient):
    """
    Client for interacting with n8n Tags APIs.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def create_tag(
        self,
        name: str
    ) -> Tag:
        """
        Create a tag in your instance.
        API Docs: https://docs.n8n.io/api/v1/tags/#create-a-tag
        """
        payload = {"name": name}
        response_data = await self.post(endpoint="/v1/tags", json=payload)
        return Tag(**response_data)

    async def list_tags(
        self,
        limit: Optional[int] = None,
        cursor: Optional[str] = None
    ) -> TagList:
        """
        Retrieve all tags from your instance.
        API Docs: https://docs.n8n.io/api/v1/tags/#retrieve-all-tags
        """
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor
        
        response_data = await self.get(endpoint="/v1/tags", params=params)
        return TagList(**response_data)

    async def get_tag(
        self,
        tag_id: str
    ) -> Tag:
        """
        Retrieves a tag.
        API Docs: https://docs.n8n.io/api/v1/tags/#retrieves-a-tag
        """
        response_data = await self.get(endpoint=f"/v1/tags/{tag_id}")
        return Tag(**response_data)

    async def delete_tag(
        self,
        tag_id: str
    ) -> Tag: # API doc states it returns the deleted tag object
        """
        Deletes a tag.
        API Docs: https://docs.n8n.io/api/v1/tags/#delete-a-tag
        """
        response_data = await self.delete(endpoint=f"/v1/tags/{tag_id}")
        return Tag(**response_data)

    async def update_tag(
        self,
        tag_id: str,
        name: str
    ) -> Tag:
        """
        Update a tag.
        API Docs: https://docs.n8n.io/api/v1/tags/#update-a-tag
        """
        payload = {"name": name}
        response_data = await self.put(endpoint=f"/v1/tags/{tag_id}", json=payload)
        return Tag(**response_data) 