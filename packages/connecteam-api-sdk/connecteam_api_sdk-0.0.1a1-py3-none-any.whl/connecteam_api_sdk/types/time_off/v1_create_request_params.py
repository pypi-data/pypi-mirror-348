# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["V1CreateRequestParams"]


class V1CreateRequestParams(TypedDict, total=False):
    end_date: Required[Annotated[str, PropertyInfo(alias="endDate")]]
    """The end time of the time off in ISO format (YYYY-MM-DD).

    End date must be similar to Start date if isAllDay set to false.
    """

    is_all_day: Required[Annotated[bool, PropertyInfo(alias="isAllDay")]]
    """Specifies the type of the time period.

    Defaults to true. If set to false, start and end time fields must be specified.
    """

    policy_type_id: Required[Annotated[str, PropertyInfo(alias="policyTypeId")]]
    """The ID of the policy type"""

    start_date: Required[Annotated[str, PropertyInfo(alias="startDate")]]
    """The start date of the time off in ISO format (YYYY-MM-DD)"""

    status: Required[Literal["approved", "pending", "denied"]]
    """The status of the time off request."""

    timezone: Required[str]
    """The timezone in Tz format (e.g. America/New_York)"""

    user_id: Required[Annotated[int, PropertyInfo(alias="userId")]]
    """The ID of the user to create the time off request"""

    employee_note: Annotated[str, PropertyInfo(alias="employeeNote")]
    """Employee note providing additional details"""

    end_time: Annotated[str, PropertyInfo(alias="endTime")]
    """The end time of the time off in ISO format (HH:MM:SS).

    This field is required if isAllDay set to false.
    """

    is_adjust_for_day_light_saving: Annotated[bool, PropertyInfo(alias="isAdjustForDayLightSaving")]
    """
    Specifies if the time given should offset the daylight savings time change if
    the time falls exactly on the daylight savings time change. Set to true only if
    the time coincides with the rollback hour, otherwise, it should remain false.
    """

    manager_note: Annotated[str, PropertyInfo(alias="managerNote")]
    """Manager note providing additional details"""

    start_time: Annotated[str, PropertyInfo(alias="startTime")]
    """The start time of the time off in ISO format (HH:MM:SS).

    This field is required if isAllDay set to false.
    """

    time_clock_id: Annotated[int, PropertyInfo(alias="timeClockId")]
    """
    The unique identifier of the time clock where the time off will be presented in
    the timesheet
    """
