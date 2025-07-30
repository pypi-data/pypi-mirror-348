"""
Schemas for account, organization, membership, and collection reference models.
"""

from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict, field_serializer

# Type Aliases

OrganizationPlan = Literal[
    'preview',  # Evaluation tier with limited features
    'developer',  # Individual developer tier for testing or hobby projects
    'starter',  # Entry-level tier for small teams or startups
    'scale',  # Scaled tier for growing teams with increased usage
    'enterprise',  # Enterprise-grade tier with custom SLAs and support
]

MembershipRole = Literal[
    'member',  # Standard member with read/write access
    'admin',  # Administrator with full management permissions
]

# Constants

ORGANIZATION_PLANS: List[OrganizationPlan] = [
    'preview',
    'developer',
    'starter',
    'scale',
    'enterprise',
]

MEMBERSHIP_ROLES: List[MembershipRole] = [
    'member',
    'admin',
]


class AccountReference(BaseModel):
    """
    Reference to a user account.

    Attributes:
        id (str): Unique account identifier.
        email (str): Account email address.
        verified (bool): Whether the email is verified.
        date_created (datetime): Account creation timestamp.
        date_updated (datetime): Last account update timestamp.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description='Unique account identifier.')
    email: str = Field(..., description='Account email address.')
    verified: bool = Field(..., description='Whether the email address is verified.')
    date_created: datetime = Field(
        ..., alias='dateCreated', description='Account creation timestamp.'
    )
    date_updated: datetime = Field(
        ..., alias='dateUpdated', description='Last account update timestamp.'
    )

    @field_serializer('date_created', mode='plain')
    def _serialize_date_created(self, dt: datetime, _info) -> str:
        """Serialize `date_created` to ISO 8601 string."""
        return dt.isoformat()

    @field_serializer('date_updated', mode='plain')
    def _serialize_date_updated(self, dt: datetime, _info) -> str:
        """Serialize `date_updated` to ISO 8601 string."""
        return dt.isoformat()


class OrganizationSnapshot(BaseModel):
    """
    Basic snapshot of an organization.

    Attributes:
        id (str): Unique organization identifier.
        name (str): Organization name.
        description (str): Brief description.
        plan (OrganizationPlan): Active subscription plan.
    """

    id: str = Field(..., description='Unique organization identifier.')
    name: str = Field(..., description='Organization name.')
    description: str = Field(..., description='Brief description of the organization.')
    plan: OrganizationPlan = Field(..., description='Active subscription plan.')


class CollectionReference(BaseModel):
    """
    Reference to a collection within an organization.

    Attributes:
        id (str): Unique collection identifier.
        name (str): Collection display name.
        date_created (datetime): Creation timestamp.
        date_updated (datetime): Last update timestamp.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description='Unique collection identifier.')
    name: str = Field(..., description='Collection display name.')
    date_created: datetime = Field(
        ..., alias='dateCreated', description='Creation timestamp.'
    )
    date_updated: datetime = Field(
        ..., alias='dateUpdated', description='Last update timestamp.'
    )

    @field_serializer('date_created', mode='plain')
    def _serialize_date_created(self, dt: datetime, _info) -> str:
        return dt.isoformat()

    @field_serializer('date_updated', mode='plain')
    def _serialize_date_updated(self, dt: datetime, _info) -> str:
        return dt.isoformat()


class MembershipBase(BaseModel):
    """
    Common membership fields for an organization.

    Attributes:
        id (str): Membership record identifier.
        account_id (str): Referenced account identifier.
        role (MembershipRole): Assigned membership role.
        date_created (datetime): When the membership was created.
        date_updated (datetime): When the membership was last updated.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description='Membership record identifier.')
    account_id: str = Field(
        ..., alias='accountId', description='Referenced account identifier.'
    )
    role: MembershipRole = Field(..., description='Assigned membership role.')
    date_created: datetime = Field(
        ..., alias='dateCreated', description='Membership creation timestamp.'
    )
    date_updated: datetime = Field(
        ..., alias='dateUpdated', description='Membership last update timestamp.'
    )

    @field_serializer('date_created', mode='plain')
    def _serialize_date_created(self, dt: datetime, _info) -> str:
        return dt.isoformat()

    @field_serializer('date_updated', mode='plain')
    def _serialize_date_updated(self, dt: datetime, _info) -> str:
        return dt.isoformat()


class OrganizationListMembership(MembershipBase):
    """
    Membership details returned in organization.list().

    Attributes:
        organization (OrganizationSnapshot): Snapshot of the organization.
        account (AccountReference): Reference to the member's account.
    """

    organization: OrganizationSnapshot = Field(
        ..., description='Organization snapshot.'
    )
    account: AccountReference = Field(..., description='Account reference.')


class OrganizationResultMembership(MembershipBase):
    """
    Membership details returned in organization.get().

    Attributes:
        organization (OrganizationSnapshot): Snapshot of the organization.
        account (dict): Simplified account info.
    """

    organization: OrganizationSnapshot = Field(
        ..., description='Organization snapshot.'
    )
    account: dict = Field(..., description='Simplified account information.')


class OrganizationListResult(BaseModel):
    """
    Summary of an organization for organization.list().

    Attributes:
        id (str): Organization unique identifier.
        name (str): Display name.
        description (str): Brief description.
        plan (OrganizationPlan): Active subscription plan.
        status (str): Operational status (e.g., 'active', 'suspended').
        date_created (datetime): Creation timestamp.
        date_updated (datetime): Last update timestamp.
        members (Optional[List[OrganizationListMembership]]): Membership records.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description='Organization unique identifier.')
    name: str = Field(..., description='Display name of the organization.')
    description: str = Field(..., description='Brief organization description.')
    plan: OrganizationPlan = Field(..., description='Active subscription plan.')
    status: str = Field(
        ..., description="Operational status (e.g., 'active', 'suspended')."
    )
    date_created: datetime = Field(
        ..., alias='dateCreated', description='Creation timestamp.'
    )
    date_updated: datetime = Field(
        ..., alias='dateUpdated', description='Last update timestamp.'
    )
    members: Optional[List[OrganizationListMembership]] = Field(
        None, description='Optional list of membership records.'
    )

    @field_serializer('date_created', mode='plain')
    def _serialize_date_created(self, dt: datetime, _info) -> str:
        return dt.isoformat()

    @field_serializer('date_updated', mode='plain')
    def _serialize_date_updated(self, dt: datetime, _info) -> str:
        return dt.isoformat()


class OrganizationResult(BaseModel):
    """
    Detailed organization info for organization.get().

    Attributes:
        id (str): Organization unique identifier.
        name (str): Display name.
        description (str): Brief description.
        plan (OrganizationPlan): Active subscription plan.
        status (str): Operational status.
        date_created (datetime): Creation timestamp.
        date_updated (datetime): Last update timestamp.
        members (List[OrganizationResultMembership]): Full membership records.
        collections (List[CollectionReference]): Collections owned.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description='Organization unique identifier.')
    name: str = Field(..., description='Display name of the organization.')
    description: str = Field(..., description='Brief organization description.')
    plan: OrganizationPlan = Field(..., description='Active subscription plan.')
    status: str = Field(..., description='Operational status.')

    date_created: datetime = Field(
        ..., alias='dateCreated', description='Creation timestamp.'
    )
    date_updated: datetime = Field(
        ..., alias='dateUpdated', description='Last update timestamp.'
    )
    members: List[OrganizationResultMembership] = Field(
        ..., description='Full list of membership records.'
    )
    collections: List[CollectionReference] = Field(
        ..., description='Collections owned by the organization.'
    )

    @field_serializer('date_created', mode='plain')
    def _serialize_date_created(self, dt: datetime, _info) -> str:
        return dt.isoformat()

    @field_serializer('date_updated', mode='plain')
    def _serialize_date_updated(self, dt: datetime, _info) -> str:
        return dt.isoformat()


class OrganizationMemberRequest(BaseModel):
    """
    Payload for inviting or updating a member in an organization.

    Attributes:
        id (str): UUID of the user or email address to invite.
        role (MembershipRole): Role to assign ('admin' or 'member').
    """

    id: str = Field(
        ..., description='UUID of the user or email address for invitation.'
    )
    role: MembershipRole = Field(
        ..., description="Role to assign: 'admin' or 'member'."
    )
