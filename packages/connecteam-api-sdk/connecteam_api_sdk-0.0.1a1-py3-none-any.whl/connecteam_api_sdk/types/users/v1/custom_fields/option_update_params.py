# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["OptionUpdateParams"]


class OptionUpdateParams(TypedDict, total=False):
    custom_field_id: Required[Annotated[int, PropertyInfo(alias="customFieldId")]]
    """The unique identifier of the custom field"""

    is_disabled: Annotated[bool, PropertyInfo(alias="isDisabled")]
    """Indicates if this option is disabled"""

    value: str
    """The value to be added as the option"""
