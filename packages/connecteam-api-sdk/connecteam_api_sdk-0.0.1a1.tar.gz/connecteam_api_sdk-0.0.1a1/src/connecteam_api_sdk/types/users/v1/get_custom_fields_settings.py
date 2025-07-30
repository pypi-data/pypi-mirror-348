# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from ...._models import BaseModel
from .user_custom_fields import UserCustomFields

__all__ = [
    "GetCustomFieldsSettings",
    "CustomField",
    "CustomFieldDropdownCustomFieldSettingsResponse",
    "CustomFieldDropdownCustomFieldSettingsResponseDropdownOption",
    "CustomFieldCustomFieldSettingsResponse",
]


class CustomFieldDropdownCustomFieldSettingsResponseDropdownOption(BaseModel):
    id: int
    """The id of this option"""

    value: str
    """The name of this option"""

    is_deleted: Optional[bool] = FieldInfo(alias="isDeleted", default=None)
    """
    Indicates if this option is deleted (this will still be returned in case someone
    already chose this option so you can see the value).
    """

    is_disabled: Optional[bool] = FieldInfo(alias="isDisabled", default=None)
    """Indicates if this option is disabled"""


class CustomFieldDropdownCustomFieldSettingsResponse(BaseModel):
    id: int
    """The custom fields id"""

    category_id: int = FieldInfo(alias="categoryId")
    """The unique identifier of the custom field category"""

    dropdown_options: List[CustomFieldDropdownCustomFieldSettingsResponseDropdownOption] = FieldInfo(
        alias="dropdownOptions"
    )
    """
    The options available for selection in the dropdown field. Applicable only to
    custom fields configured as dropdown types.
    """

    is_editable_for_all_admins: bool = FieldInfo(alias="isEditableForAllAdmins")
    """Indicates whether the custom field is editable by all admins"""

    is_editable_for_users: bool = FieldInfo(alias="isEditableForUsers")
    """
    Indicates whether the custom field is editable by users. Applicable only to
    custom fields that are visible to users.
    """

    is_multi_select: bool = FieldInfo(alias="isMultiSelect")
    """
    Indicates whether multiple selections are allowed in the dropdown. Applicable
    only to custom fields configured as dropdown types.
    """

    is_required: bool = FieldInfo(alias="isRequired")
    """Indicates whether the custom field is required"""

    is_visible_to_all_admins: bool = FieldInfo(alias="isVisibleToAllAdmins")
    """Indicates whether the custom field is visible to all admins"""

    is_visible_to_users: bool = FieldInfo(alias="isVisibleToUsers")
    """Indicates whether the custom field is visible to users"""

    name: str
    """The name of the custom field"""

    edit_access_admin_ids: Optional[List[int]] = FieldInfo(alias="editAccessAdminIds", default=None)
    """
    A list of unique identifiers of the admins who will be granted access to edit
    this custom field, owners can always edit all custom fields. Applicable only to
    custom fields that are not editable by all admins.
    """

    type: Optional[Literal["dropdown"]] = None
    """
    The type of the custom field: Email, Date, Number, Text, Phone number, Dropdown,
    File.
    """

    view_access_admin_ids: Optional[List[int]] = FieldInfo(alias="viewAccessAdminIds", default=None)
    """
    A list of unique identifiers of the admins who will be granted access to view
    this custom field, owners can always see all custom fields. Applicable only to
    custom fields that are not visible to all admins.
    """


class CustomFieldCustomFieldSettingsResponse(BaseModel):
    id: int
    """The custom fields id"""

    category_id: int = FieldInfo(alias="categoryId")
    """The unique identifier of the custom field category"""

    is_editable_for_all_admins: bool = FieldInfo(alias="isEditableForAllAdmins")
    """Indicates whether the custom field is editable by all admins"""

    is_editable_for_users: bool = FieldInfo(alias="isEditableForUsers")
    """
    Indicates whether the custom field is editable by users. Applicable only to
    custom fields that are visible to users.
    """

    is_required: bool = FieldInfo(alias="isRequired")
    """Indicates whether the custom field is required"""

    is_visible_to_all_admins: bool = FieldInfo(alias="isVisibleToAllAdmins")
    """Indicates whether the custom field is visible to all admins"""

    is_visible_to_users: bool = FieldInfo(alias="isVisibleToUsers")
    """Indicates whether the custom field is visible to users"""

    name: str
    """The name of the custom field"""

    type: UserCustomFields
    """An enumeration."""

    edit_access_admin_ids: Optional[List[int]] = FieldInfo(alias="editAccessAdminIds", default=None)
    """
    A list of unique identifiers of the admins who will be granted access to edit
    this custom field, owners can always edit all custom fields. Applicable only to
    custom fields that are not editable by all admins.
    """

    view_access_admin_ids: Optional[List[int]] = FieldInfo(alias="viewAccessAdminIds", default=None)
    """
    A list of unique identifiers of the admins who will be granted access to view
    this custom field, owners can always see all custom fields. Applicable only to
    custom fields that are not visible to all admins.
    """


CustomField: TypeAlias = Union[CustomFieldDropdownCustomFieldSettingsResponse, CustomFieldCustomFieldSettingsResponse]


class GetCustomFieldsSettings(BaseModel):
    custom_fields: List[CustomField] = FieldInfo(alias="customFields")
    """The custom fields."""
