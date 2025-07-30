# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal, Annotated, TypedDict

from ...._utils import PropertyInfo
from .user_custom_fields import UserCustomFields
from ...scheduler.v1.schedulers.sort_order import SortOrder

__all__ = ["CustomFieldListParams"]


class CustomFieldListParams(TypedDict, total=False):
    category_ids: Annotated[Iterable[int], PropertyInfo(alias="categoryIds")]
    """Custom field category ids to filter by"""

    custom_field_ids: Annotated[Iterable[int], PropertyInfo(alias="customFieldIds")]
    """Custom field ids to filter by"""

    custom_field_names: Annotated[List[str], PropertyInfo(alias="customFieldNames")]
    """Custom field names to filter by"""

    custom_field_types: Annotated[List[UserCustomFields], PropertyInfo(alias="customFieldTypes")]
    """Custom field types to filter by"""

    limit: int
    """The maximum number of results to display per page"""

    offset: int
    """
    The resource offset of the last successfully read resource will be returned as
    the paging.offset JSON property of a paginated response containing more results
    """

    order: SortOrder
    """An enumeration."""

    sort: Literal["id", "name", "type"]
    """An enumeration."""
