# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["UserUpdatePerformanceParams", "Item"]


class UserUpdatePerformanceParams(TypedDict, total=False):
    user_id: Required[Annotated[int, PropertyInfo(alias="userId")]]
    """The ID of the user whose data is being accessed or modified"""

    items: Required[Iterable[Item]]
    """List of performance data values to update"""


class Item(TypedDict, total=False):
    indicator_id: Required[Annotated[int, PropertyInfo(alias="indicatorId")]]
    """ID of the performance indicator/metric"""

    value: Required[float]
    """Value for the performance indicator/metric"""
