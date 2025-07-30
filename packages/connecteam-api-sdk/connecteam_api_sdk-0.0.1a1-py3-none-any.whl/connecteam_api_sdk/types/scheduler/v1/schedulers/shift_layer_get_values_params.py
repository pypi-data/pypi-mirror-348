# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["ShiftLayerGetValuesParams"]


class ShiftLayerGetValuesParams(TypedDict, total=False):
    scheduler_id: Required[Annotated[int, PropertyInfo(alias="schedulerId")]]
    """The unique identifier of the scheduler"""

    limit: int
    """The maximum number of results to display per page"""

    offset: int
    """
    The resource offset of the last successfully read resource will be returned as
    the paging.offset JSON property of a paginated response containing more results
    """
