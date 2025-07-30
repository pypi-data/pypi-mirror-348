from typing import List, Optional

from gestell.service.base import BaseService
from gestell.types import BaseResponse, OrganizationMemberRequest
from gestell.organization.get import (
    GetOrganizationRequest,
    GetOrganizationResponse,
    get_organization,
)
from gestell.organization.list import (
    GetOrganizationsRequest,
    GetOrganizationsResponse,
    list_organizations,
)
from gestell.organization.update import (
    UpdateOrganizationRequest,
    UpdateOrganizationResponse,
    update_organization,
)
from gestell.organization.members.add import (
    AddMembersRequest,
    AddMembersResponse,
    add_members,
)
from gestell.organization.members.remove import (
    RemoveMembersRequest,
    RemoveMembersResponse,
    remove_members,
)


class OrganizationService(BaseService):
    """
    Manages organizations you are a part of.

    Learn more about usage at: https://gestell.ai/docs/reference#organization
    """

    def __init__(self, api_key: str, api_url: str, debug: bool = False) -> None:
        super().__init__(api_key, api_url, debug)

    async def get(self, id: str) -> GetOrganizationResponse:
        """Retrieve details of a specific organization.

        Learn more about usage at: https://gestell.ai/docs/reference#organization

        Fetches comprehensive information about an organization, including its members,
        collections, and metadata. The organization must be accessible by the current user.

        Args:
            id: The unique identifier of the organization to retrieve.

        Returns:
            GetOrganizationResponse: An object containing the organization details.

        Raises:
            GestellError: If the request fails or the organization is not found.

        Example:
            ```python
            response = await org_service.get(id='org_123')
            print(f'Organization: {response.result.name}')
            print(f'Members: {len(response.result.members)}')
            print(f'Collections: {len(response.result.collections)}')
            ```
        """
        request = GetOrganizationRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            id=id,
        )
        response: GetOrganizationResponse = await get_organization(request)
        return response

    async def list(
        self,
        search: Optional[str] = None,
        take: Optional[int] = 10,
        skip: Optional[int] = 0,
        extended: Optional[bool] = None,
    ) -> GetOrganizationsResponse:
        """List organizations accessible to the current user.

        Learn more about usage at: https://gestell.ai/docs/reference#organization

        Retrieves a paginated list of organizations that the authenticated user has access to.
        The results can be filtered and paginated as needed.

        Args:
            search: Optional search query to filter organizations by name or description.
            take: Maximum number of organizations to return. Defaults to 10.
            skip: Number of organizations to skip for pagination. Defaults to 0.
            extended: If True, includes additional details like members and collections
                     for each organization. This may increase response time.

        Returns:
            GetOrganizationsResponse: An object containing the list of organizations and pagination info.

        Raises:
            GestellError: If the request fails due to authentication or other issues.

        Example:
            ```python
            # Get first page of organizations
            response = await org_service.list()

            # Search for organizations
            search_results = await org_service.list(search='research', take=5)

            # Get extended details with pagination
            orgs_page_2 = await org_service.list(take=20, skip=20, extended=True)
            ```
        """
        request = GetOrganizationsRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            search=search,
            take=take,
            skip=skip,
            extended=extended,
        )
        response: GetOrganizationsResponse = await list_organizations(request)
        return response

    async def update(
        self,
        id: str,
        name: str,
        description: str,
    ) -> UpdateOrganizationResponse:
        """Update an organization's details.

        Learn more about usage at: https://gestell.ai/docs/reference#organization

        Modifies the name and/or description of an existing organization.
        The authenticated user must have admin privileges for the organization.

        Args:
            id: The unique identifier of the organization to update.
            name: The new name for the organization.
            description: The new description for the organization.

        Returns:
            UpdateOrganizationResponse: An object containing the status of the update operation.

        Raises:
            GestellError: If the update fails, the organization is not found,
                         or the user lacks permission.

        Example:
            ```python
            response = await org_service.update(
                id='org_123',
                name='New Organization Name',
                description='Updated organization description',
            )
            if response.status == 'OK':
                print('Organization updated successfully')
            ```
        """
        request = UpdateOrganizationRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            id=id,
            name=name,
            description=description,
        )
        response: UpdateOrganizationResponse = await update_organization(request)
        return response

    async def add_members(
        self, id: str, members: List[OrganizationMemberRequest]
    ) -> BaseResponse:
        """Add members to an organization.

        Learn more about usage at: https://gestell.ai/docs/reference#organization

        Invites one or more users to join the organization with specified roles.
        Users can be invited by their email address or user ID. If a user doesn't
        exist with the provided email, an invitation will be sent.

        Args:
            id: The unique identifier of the organization.
            members: A list of member objects, each containing:
                - id: The user's email address or existing user ID.
                - role: The role to assign ('member' or 'admin').

        Returns:
            BaseResponse: An object containing the status of the operation.

        Raises:
            GestellError: If the request fails, the organization is not found,
                         or the user lacks permission.

        Example:
            ```python
            from gestell.types.organization import OrganizationMemberRequest

            # Add multiple members with different roles
            new_members = [
                OrganizationMemberRequest(id='user@example.com', role='admin'),
                OrganizationMemberRequest(id='another@example.com', role='member'),
            ]
            response = await org_service.add_members(id='org_123', members=new_members)
            ```
        """
        request = AddMembersRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            id=id,
            members=members,
        )
        response: AddMembersResponse = await add_members(request)
        return response

    async def remove_members(self, id: str, members: List[str]) -> BaseResponse:
        """Remove members from an organization.

        Learn more about usage at: https://gestell.ai/docs/reference#organization

        Removes one or more members from the organization. This operation is immediate
        and cannot be undone. The last admin cannot be removed until another admin is designated.

        Args:
            id: The unique identifier of the organization.
            members: A list of user IDs or email addresses to remove from the organization.

        Returns:
            BaseResponse: An object containing the status of the operation.

        Raises:
            GestellError: If the request fails, the organization is not found,
                         the user lacks permission, or trying to remove the last admin.

        Example:
            ```python
            # Remove members by their user IDs or emails
            response = await org_service.remove_members(
                id='org_123', members=['user1@example.com', 'user2@example.com']
            )

            if response.status == 'OK':
                print('Members removed successfully')
            ```
        """
        request = RemoveMembersRequest(
            api_key=self.api_key,
            api_url=self.api_url,
            debug=self.debug,
            id=id,
            members=members,
        )
        response: RemoveMembersResponse = await remove_members(request)
        return response
