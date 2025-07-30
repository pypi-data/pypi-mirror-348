# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from ....._utils import PropertyInfo
from .timestamp_with_timezone_activity_param import TimestampWithTimezoneActivityParam

__all__ = ["TimeActivityCreateParams", "TimeActivity", "TimeActivityShift", "TimeActivityManualbreak"]


class TimeActivityCreateParams(TypedDict, total=False):
    time_activities: Required[Annotated[Iterable[TimeActivity], PropertyInfo(alias="timeActivities")]]
    """List of the time activities of the users"""


class TimeActivityShift(TypedDict, total=False):
    job_id: Required[Annotated[str, PropertyInfo(alias="jobId")]]
    """The job ID of the shift"""

    start: Required[TimestampWithTimezoneActivityParam]
    """The start time"""

    employee_note: Annotated[str, PropertyInfo(alias="employeeNote")]
    """Employee note providing additional details"""

    end: TimestampWithTimezoneActivityParam
    """The end time"""

    manager_note: Annotated[str, PropertyInfo(alias="managerNote")]
    """Manager note providing additional details"""

    sub_job_id: Annotated[str, PropertyInfo(alias="subJobId")]
    """The sub job ID of the shift.

    Required if sub jobs are defined under the specific job
    """


class TimeActivityManualbreak(TypedDict, total=False):
    id: Required[str]
    """The ID of the manual break"""

    start: Required[TimestampWithTimezoneActivityParam]
    """The start time"""

    employee_note: Annotated[str, PropertyInfo(alias="employeeNote")]
    """Employee note providing additional details"""

    end: TimestampWithTimezoneActivityParam
    """The end time"""

    manager_note: Annotated[str, PropertyInfo(alias="managerNote")]
    """Manager note providing additional details"""


class TimeActivity(TypedDict, total=False):
    shifts: Required[Iterable[TimeActivityShift]]
    """The new shifts"""

    user_id: Required[Annotated[int, PropertyInfo(alias="userId")]]
    """The user ID of the time activity"""

    manualbreaks: Iterable[TimeActivityManualbreak]
    """The new manual breaks"""
