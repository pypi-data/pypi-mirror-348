# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["OptionListParams"]


class OptionListParams(TypedDict, total=False):
    is_deleted: Annotated[bool, PropertyInfo(alias="isDeleted")]
    """Parameter specifying the if to filter only for deleted options."""

    is_disabled: Annotated[bool, PropertyInfo(alias="isDisabled")]
    """Parameter specifying the if to filter only for disabled options."""

    limit: int
    """The maximum number of results to display per page"""

    offset: int
    """
    The resource offset of the last successfully read resource will be returned as
    the paging.offset JSON property of a paginated response containing more results
    """
