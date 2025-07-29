"""
n8n User API Client.
"""

from typing import Optional, Any

from ..client.base import BaseClient
from ..models.users import (
    UsersList, UserCreateItem, UserCreateResponseItem, User, UserRole
)
from ..models.base import N8nBaseModel # For generic response like operation status


class UserClient(BaseClient):
    """
    Client for interacting with n8n User APIs.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def list_users(
        self,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        include_role: Optional[bool] = None,
        project_id: Optional[str] = None
    ) -> UsersList:
        """
        Retrieve all users from your instance. Only available for the instance owner.
        API Docs: https://docs.n8n.io/api/v1/users/#retrieve-all-users
        """
        params = {}
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor
        if include_role is not None:
            params["includeRole"] = include_role
        if project_id is not None:
            params["projectId"] = project_id
        
        response_data = await self.get(endpoint="/v1/users", params=params)
        return UsersList(**response_data)

    async def create_users(
        self,
        users: list[UserCreateItem | dict[str, Any]]
    ) -> list[UserCreateResponseItem]:
        """
        Create one or more users.
        API Docs: https://docs.n8n.io/api/v1/users/#create-multiple-users
        """
        _users: list[UserCreateItem] = []
        for user_input_item in users:
            if isinstance(user_input_item, dict):
                _users.append(UserCreateItem(**user_input_item))
            elif isinstance(user_input_item, UserCreateItem):
                _users.append(user_input_item)
            else:
                raise TypeError(
                    "Each item in 'users' list must be a UserCreateItem instance or a dict, "
                    f"got {type(user_input_item).__name__} for item {user_input_item!r}"
                )
        
        # Convert list[UserCreateItem] to list[Dict] for the JSON body
        users_payload = [user.model_dump(exclude_none=True) for user in _users]
        response_data = await self.post(endpoint="/v1/users", json=users_payload)
        # Assuming the response is a list of dictionaries, each can be parsed into UserCreateResponseItem
        return [UserCreateResponseItem(**item) for item in response_data]

    async def get_user(
        self,
        user_id_or_email: str,
        include_role: Optional[bool] = None
    ) -> User:
        """
        Retrieve a user from your instance by ID or email.
        API Docs: https://docs.n8n.io/api/v1/users/#get-user-by-id-email
        """
        params = {}
        if include_role is not None:
            params["includeRole"] = include_role
            
        response_data = await self.get(endpoint=f"/v1/users/{user_id_or_email}", params=params)
        return User(**response_data)

    async def delete_user(
        self,
        user_id_or_email: str
    ) -> None: # API returns 204 No Content
        """
        Delete a user from your instance.
        API Docs: https://docs.n8n.io/api/v1/users/#delete-a-user
        """
        await self.delete(endpoint=f"/v1/users/{user_id_or_email}")
        # For 204 No Content, typically no specific model is returned, or a generic success message model.
        # Here, returning None as per API spec. A custom model for operation status could also be used.
        return None

    async def update_user_role(
        self,
        user_id_or_email: str,
        new_role: UserRole | str
    ) -> None: # API returns 200 with no specific body in docs for success, implies operation status
        """
        Change a user's global role.
        API Docs: https://docs.n8n.io/api/v1/users/#change-a-user-s-global-role
        """
        _new_role: UserRole
        if isinstance(new_role, str):
            try:
                _new_role = UserRole(new_role)
            except ValueError as e:
                raise TypeError(f"Invalid string value for UserRole: '{new_role}'. Valid values are: {[r.value for r in UserRole]}. Error: {e}") from e
        elif isinstance(new_role, UserRole):
            _new_role = new_role
        else:
            raise TypeError(f"'new_role' must be a UserRole instance or a str, got {type(new_role).__name__}")

        payload = {"newRoleName": _new_role.value}
        await self.patch(endpoint=f"/v1/users/{user_id_or_email}/role", json=payload)
        # Similar to delete, API docs don't specify a clear response model for success, often it's just a status.
        # Returning None for now.
        return None 