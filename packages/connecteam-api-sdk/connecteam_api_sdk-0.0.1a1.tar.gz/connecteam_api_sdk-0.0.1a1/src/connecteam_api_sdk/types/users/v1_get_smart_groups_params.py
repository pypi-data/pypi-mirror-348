# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["V1GetSmartGroupsParams"]


class V1GetSmartGroupsParams(TypedDict, total=False):
    id: int
    """The unique identifier of the smart group."""

    name: str
    """The name of the smart group to filter by."""
