# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .user_type import UserType
from ...._models import BaseModel
from .user_custom_fields import UserCustomFields

__all__ = ["User", "CustomField"]


class CustomField(BaseModel):
    custom_field_id: int = FieldInfo(alias="customFieldId")
    """The custom field unique id"""

    name: str
    """The custom field name"""

    type: UserCustomFields
    """An enumeration."""

    value: object
    """The value of the custom field.

    Our real-time API documentation experience does not support custom fields of the
    dropdown type.To update dropdown fields value(s), pass an array of objects with
    the IDs of the selected dropdown values (e.g., [{id: 1}, {id: 2}]).
    """


class User(BaseModel):
    first_name: str = FieldInfo(alias="firstName")
    """The user's first name"""

    last_name: str = FieldInfo(alias="lastName")
    """The user's last name"""

    phone_number: str = FieldInfo(alias="phoneNumber")
    """The user's phone number"""

    user_id: int = FieldInfo(alias="userId")
    """The user's unique id"""

    user_type: UserType = FieldInfo(alias="userType")
    """An enumeration."""

    archived_at: Optional[int] = FieldInfo(alias="archivedAt", default=None)
    """The timestamp when the user was archived in the system"""

    created_at: Optional[int] = FieldInfo(alias="createdAt", default=None)
    """The timestamp when the user was first created in the system"""

    custom_fields: Optional[List[CustomField]] = FieldInfo(alias="customFields", default=None)
    """The user's custom fields"""

    email: Optional[str] = None
    """The user's email (mandatory for managers and owners)"""

    invited_to_be_manager: Optional[bool] = FieldInfo(alias="invitedToBeManager", default=None)
    """Is the user invited to be a manager"""

    is_archived: Optional[bool] = FieldInfo(alias="isArchived", default=None)
    """The user's archived status"""

    kiosk_code: Optional[str] = FieldInfo(alias="kioskCode", default=None)
    """The code for the user to access the kiosk app"""

    last_login: Optional[int] = FieldInfo(alias="lastLogin", default=None)
    """The last login timestamp of the user in the system"""

    modified_at: Optional[int] = FieldInfo(alias="modifiedAt", default=None)
    """The timestamp of the most recent change to any user field"""

    smart_groups_ids: Optional[List[int]] = FieldInfo(alias="smartGroupsIds", default=None)
    """The user's smart groups he is a member of"""
