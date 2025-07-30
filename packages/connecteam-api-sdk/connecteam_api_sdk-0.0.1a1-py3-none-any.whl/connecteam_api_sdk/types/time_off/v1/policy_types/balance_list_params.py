# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["BalanceListParams"]


class BalanceListParams(TypedDict, total=False):
    limit: int
    """The maximum number of results to display per page"""

    offset: int
    """
    The resource offset of the last successfully read resource will be returned as
    the paging.offset JSON property of a paginated response containing more results
    """

    user_ids: Annotated[Iterable[int], PropertyInfo(alias="userIds")]
    """List of user ids"""
