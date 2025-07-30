# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["SchedulerGetUserUnavailabilitiesParams"]


class SchedulerGetUserUnavailabilitiesParams(TypedDict, total=False):
    end_time: Required[Annotated[int, PropertyInfo(alias="endTime")]]
    """The end time to filter by in Unix format (in seconds)"""

    start_time: Required[Annotated[int, PropertyInfo(alias="startTime")]]
    """The start time to filter by in Unix format (in seconds)"""

    user_id: Required[Annotated[int, PropertyInfo(alias="userId")]]
    """The unique identifier of the user"""
