# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo
from .user_type import UserType
from .base_custom_field_param import BaseCustomFieldParam

__all__ = ["UserUpdateParams", "Body"]


class UserUpdateParams(TypedDict, total=False):
    body: Required[Iterable[Body]]
    """List of users to edit."""

    edit_users_by_phone: Annotated[bool, PropertyInfo(alias="editUsersByPhone")]
    """Optional flag to edit users by phone (default by user id)."""

    include_smart_group_ids: Annotated[bool, PropertyInfo(alias="includeSmartGroupIds")]
    """
    Indicates whether to include smart group IDs in the response body for the
    updated user(s). Please note that setting this value to true may increase the
    request time significantly.
    """


class Body(TypedDict, total=False):
    custom_fields: Annotated[Iterable[BaseCustomFieldParam], PropertyInfo(alias="customFields")]
    """The user's custom fields"""

    email: str
    """The user's email (mandatory for managers and owners)"""

    first_name: Annotated[str, PropertyInfo(alias="firstName")]
    """The user's first name"""

    is_archived: Annotated[bool, PropertyInfo(alias="isArchived")]
    """
    The user status.Note that restoring a user is not applicable with the
    editUserByPhone field (you must provide the user ID).
    """

    last_name: Annotated[str, PropertyInfo(alias="lastName")]
    """The user's last name"""

    phone_number: Annotated[str, PropertyInfo(alias="phoneNumber")]
    """The user's phone number"""

    user_id: Annotated[int, PropertyInfo(alias="userId")]
    """The user's unique id"""

    user_type: Annotated[UserType, PropertyInfo(alias="userType")]
    """An enumeration."""
