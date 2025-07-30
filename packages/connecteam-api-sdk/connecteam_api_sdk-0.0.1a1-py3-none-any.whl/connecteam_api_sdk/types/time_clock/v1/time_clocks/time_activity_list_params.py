# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["TimeActivityListParams"]


class TimeActivityListParams(TypedDict, total=False):
    end_date: Required[Annotated[str, PropertyInfo(alias="endDate")]]
    """The end time to filter by in ISO 8601 format (YYYY-MM-DD)"""

    start_date: Required[Annotated[str, PropertyInfo(alias="startDate")]]
    """The start time to filter by in ISO 8601 format (YYYY-MM-DD)"""

    activity_types: Annotated[List[Literal["shift", "manual_break", "time_off"]], PropertyInfo(alias="activityTypes")]
    """The time activity types: shift, manual_break or time_off"""

    job_ids: Annotated[List[str], PropertyInfo(alias="jobIds")]
    """The job IDs of shifts"""

    manual_break_ids: Annotated[List[str], PropertyInfo(alias="manualBreakIds")]
    """The manual break IDs of manual breaks"""

    policy_type_ids: Annotated[List[str], PropertyInfo(alias="policyTypeIds")]
    """The policy type IDs of time offs"""

    user_ids: Annotated[Iterable[int], PropertyInfo(alias="userIds")]
    """Filter time activities by a list of user IDs.

    Users who are no longer assigned to the specified time clock cannot be retrieved
    with this filter.
    """
