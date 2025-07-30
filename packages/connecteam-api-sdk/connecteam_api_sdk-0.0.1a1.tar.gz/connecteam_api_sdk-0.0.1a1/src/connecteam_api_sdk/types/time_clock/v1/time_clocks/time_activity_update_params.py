# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from ....._utils import PropertyInfo
from .timestamp_with_timezone_activity_param import TimestampWithTimezoneActivityParam

__all__ = ["TimeActivityUpdateParams", "TimeActivity", "TimeActivityShift", "TimeActivityManualbreak"]


class TimeActivityUpdateParams(TypedDict, total=False):
    time_activities: Required[Annotated[Iterable[TimeActivity], PropertyInfo(alias="timeActivities")]]
    """List of time activities of the users"""


class TimeActivityShift(TypedDict, total=False):
    id: Required[str]
    """The ID of the time activity associated with the time clock"""

    employee_note: Annotated[str, PropertyInfo(alias="employeeNote")]
    """Employee note providing additional details"""

    end: TimestampWithTimezoneActivityParam
    """The end time of the time activity"""

    job_id: Annotated[str, PropertyInfo(alias="jobId")]
    """
    The job ID to associate with the shift (if the shift remains under the same job
    leave it empty)
    """

    manager_note: Annotated[str, PropertyInfo(alias="managerNote")]
    """Manager note providing additional details"""

    start: TimestampWithTimezoneActivityParam
    """The start time of the time activity"""

    sub_job_id: Annotated[str, PropertyInfo(alias="subJobId")]
    """
    The sub-job ID to associate with the job (if the sub-job remains under the same
    parent job update only the sub-job ID)
    """


class TimeActivityManualbreak(TypedDict, total=False):
    id: Required[str]
    """The ID of the time activity associated with the time clock"""

    employee_note: Annotated[str, PropertyInfo(alias="employeeNote")]
    """Employee note providing additional details"""

    end: TimestampWithTimezoneActivityParam
    """The end time of the time activity"""

    manager_note: Annotated[str, PropertyInfo(alias="managerNote")]
    """Manager note providing additional details"""

    manual_break_id: Annotated[str, PropertyInfo(alias="manualBreakId")]
    """The manual break ID to associate with the break"""

    start: TimestampWithTimezoneActivityParam
    """The start time of the time activity"""


class TimeActivity(TypedDict, total=False):
    shifts: Required[Iterable[TimeActivityShift]]
    """The shifts to update"""

    user_id: Required[Annotated[int, PropertyInfo(alias="userId")]]
    """The user ID of the time activity"""

    manualbreaks: Iterable[TimeActivityManualbreak]
    """The breaks to update"""
