# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["CustomFieldUpdateParams", "CustomField", "CustomFieldDropdownOption"]


class CustomFieldUpdateParams(TypedDict, total=False):
    custom_fields: Required[Annotated[Iterable[CustomField], PropertyInfo(alias="customFields")]]
    """The custom fields."""


class CustomFieldDropdownOption(TypedDict, total=False):
    id: int
    """The id of this option"""

    is_deleted: Annotated[bool, PropertyInfo(alias="isDeleted")]
    """
    Indicates if this option is deleted (this will still be returned in case someone
    already chose this option so you can see the value).
    """

    is_disabled: Annotated[bool, PropertyInfo(alias="isDisabled")]
    """Indicates if this option is disabled"""

    value: str
    """The name of this option"""


class CustomField(TypedDict, total=False):
    id: Required[int]
    """The custom fields id"""

    category_id: Annotated[int, PropertyInfo(alias="categoryId")]
    """The unique identifier of the custom field category"""

    dropdown_options: Annotated[Iterable[CustomFieldDropdownOption], PropertyInfo(alias="dropdownOptions")]
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

    is_editable_for_all_admins: Annotated[bool, PropertyInfo(alias="isEditableForAllAdmins")]
    """Indicates whether the custom field is editable by all admins"""

    is_editable_for_users: Annotated[bool, PropertyInfo(alias="isEditableForUsers")]
    """
    Indicates whether the custom field is editable by users. Applicable only to
    custom fields that are visible to users.
    """

    is_multi_select: Annotated[bool, PropertyInfo(alias="isMultiSelect")]
    """
    Indicates whether multiple selections are allowed in the dropdown. Applicable
    only to custom fields configured as dropdown types.
    """

    is_required: Annotated[bool, PropertyInfo(alias="isRequired")]
    """Indicates whether the custom field is required"""

    is_visible_to_all_admins: Annotated[bool, PropertyInfo(alias="isVisibleToAllAdmins")]
    """Indicates whether the custom field is visible to all admins"""

    is_visible_to_users: Annotated[bool, PropertyInfo(alias="isVisibleToUsers")]
    """Indicates whether the custom field is visible to users"""

    name: str
    """The name of the custom field"""

    view_access_admin_ids: Annotated[Iterable[int], PropertyInfo(alias="viewAccessAdminIds")]
    """
    A list of unique identifiers of the admins who will be granted access to view
    this custom field, owners can always see all custom fields. Applicable only to
    custom fields that are not visible to all admins.
    """
