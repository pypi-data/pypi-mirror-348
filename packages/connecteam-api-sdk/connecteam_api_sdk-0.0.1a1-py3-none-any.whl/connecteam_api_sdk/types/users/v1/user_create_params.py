# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo
from .user_type import UserType
from .base_custom_field_param import BaseCustomFieldParam

__all__ = ["UserCreateParams", "Body"]


class UserCreateParams(TypedDict, total=False):
    body: Required[Iterable[Body]]
    """List of users to create."""

    send_activation: Annotated[bool, PropertyInfo(alias="sendActivation")]
    """Optional flag to send activation sms."""


class Body(TypedDict, total=False):
    first_name: Required[Annotated[str, PropertyInfo(alias="firstName")]]
    """The user's first name"""

    last_name: Required[Annotated[str, PropertyInfo(alias="lastName")]]
    """The user's last name"""

    phone_number: Required[Annotated[str, PropertyInfo(alias="phoneNumber")]]
    """The user's phone number"""

    user_type: Required[Annotated[UserType, PropertyInfo(alias="userType")]]
    """An enumeration."""

    custom_fields: Annotated[Iterable[BaseCustomFieldParam], PropertyInfo(alias="customFields")]
    """The user's custom fields"""

    email: str
    """The user's email (mandatory for managers and owners)"""

    is_archived: Annotated[bool, PropertyInfo(alias="isArchived")]
    """The user's archived status"""
