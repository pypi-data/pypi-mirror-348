# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from ...._utils import PropertyInfo
from .custom_fields.create_dropdown_custom_field_option_param import CreateDropdownCustomFieldOptionParam

__all__ = [
    "CustomFieldCreateParams",
    "CustomField",
    "CustomFieldDropdownCustomFieldCreateRequest",
    "CustomFieldCustomFieldCreateRequest",
]


class CustomFieldCreateParams(TypedDict, total=False):
    custom_fields: Required[Annotated[Iterable[CustomField], PropertyInfo(alias="customFields")]]
    """The custom fields."""


class CustomFieldDropdownCustomFieldCreateRequest(TypedDict, total=False):
    category_id: Required[Annotated[int, PropertyInfo(alias="categoryId")]]
    """The unique identifier of the custom field category"""

    is_editable_for_all_admins: Required[Annotated[bool, PropertyInfo(alias="isEditableForAllAdmins")]]
    """Indicates whether the custom field is editable by all admins"""

    is_editable_for_users: Required[Annotated[bool, PropertyInfo(alias="isEditableForUsers")]]
    """
    Indicates whether the custom field is editable by users. Applicable only to
    custom fields that are visible to users.
    """

    is_multi_select: Required[Annotated[bool, PropertyInfo(alias="isMultiSelect")]]
    """
    Indicates whether multiple selections are allowed in the dropdown. Applicable
    only to custom fields configured as dropdown types.
    """

    is_required: Required[Annotated[bool, PropertyInfo(alias="isRequired")]]
    """Indicates whether the custom field is required"""

    is_visible_to_all_admins: Required[Annotated[bool, PropertyInfo(alias="isVisibleToAllAdmins")]]
    """Indicates whether the custom field is visible to all admins"""

    is_visible_to_users: Required[Annotated[bool, PropertyInfo(alias="isVisibleToUsers")]]
    """Indicates whether the custom field is visible to users"""

    name: Required[str]
    """The name of the custom field"""

    dropdown_options: Annotated[Iterable[CreateDropdownCustomFieldOptionParam], PropertyInfo(alias="dropdownOptions")]
    """
    The options available for selection in the dropdown field. Applicable only to
    custom fields configured as dropdown types.
    """

    edit_access_admin_ids: Annotated[Iterable[int], PropertyInfo(alias="editAccessAdminIds")]
    """
    A list of unique identifiers of the admins who will be granted access to edit
    this custom field, owners can always edit all custom fields. Applicable only to
    custom fields that are not editable by all admins.
    """

    type: Literal["dropdown"]
    """The type of the custom field: Dropdown"""

    view_access_admin_ids: Annotated[Iterable[int], PropertyInfo(alias="viewAccessAdminIds")]
    """
    A list of unique identifiers of the admins who will be granted access to view
    this custom field, owners can always see all custom fields. Applicable only to
    custom fields that are not visible to all admins.
    """


class CustomFieldCustomFieldCreateRequest(TypedDict, total=False):
    category_id: Required[Annotated[int, PropertyInfo(alias="categoryId")]]
    """The unique identifier of the custom field category"""

    is_editable_for_all_admins: Required[Annotated[bool, PropertyInfo(alias="isEditableForAllAdmins")]]
    """Indicates whether the custom field is editable by all admins"""

    is_editable_for_users: Required[Annotated[bool, PropertyInfo(alias="isEditableForUsers")]]
    """
    Indicates whether the custom field is editable by users. Applicable only to
    custom fields that are visible to users.
    """

    is_required: Required[Annotated[bool, PropertyInfo(alias="isRequired")]]
    """Indicates whether the custom field is required"""

    is_visible_to_all_admins: Required[Annotated[bool, PropertyInfo(alias="isVisibleToAllAdmins")]]
    """Indicates whether the custom field is visible to all admins"""

    is_visible_to_users: Required[Annotated[bool, PropertyInfo(alias="isVisibleToUsers")]]
    """Indicates whether the custom field is visible to users"""

    name: Required[str]
    """The name of the custom field"""

    type: Required[Literal["email", "date", "phone", "number", "str", "file", "directManager", "birthday"]]
    """The type of the custom field: Email, Date, Number, Text, Phone number, File."""

    edit_access_admin_ids: Annotated[Iterable[int], PropertyInfo(alias="editAccessAdminIds")]
    """
    A list of unique identifiers of the admins who will be granted access to edit
    this custom field, owners can always edit all custom fields. Applicable only to
    custom fields that are not editable by all admins.
    """

    view_access_admin_ids: Annotated[Iterable[int], PropertyInfo(alias="viewAccessAdminIds")]
    """
    A list of unique identifiers of the admins who will be granted access to view
    this custom field, owners can always see all custom fields. Applicable only to
    custom fields that are not visible to all admins.
    """


CustomField: TypeAlias = Union[CustomFieldDropdownCustomFieldCreateRequest, CustomFieldCustomFieldCreateRequest]
