# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["V1CreateRequestResponse", "Data"]


class Data(BaseModel):
    id: str
    """The unique identifier of the time off request"""

    end_date: str = FieldInfo(alias="endDate")
    """The end date of the time off"""

    end_time: str = FieldInfo(alias="endTime")
    """The end time of the time off"""

    is_all_day: bool = FieldInfo(alias="isAllDay")
    """Indicates whether the time off is for the entire day"""

    policy_type_id: str = FieldInfo(alias="policyTypeId")
    """The policy type id"""

    start_date: str = FieldInfo(alias="startDate")
    """The start date of the time off"""

    start_time: str = FieldInfo(alias="startTime")
    """The start time of the time off"""

    status: Literal["approved", "pending", "denied"]
    """The status of the time off"""

    timezone: str
    """The timezone of the time off"""

    user_id: int = FieldInfo(alias="userId")
    """The user id"""

    employee_note: Optional[str] = FieldInfo(alias="employeeNote", default=None)
    """The employee note of the time off"""

    manager_note: Optional[str] = FieldInfo(alias="managerNote", default=None)
    """The manager note of the time off"""

    time_clock_id: Optional[int] = FieldInfo(alias="timeClockId", default=None)
    """
    The unique identifier of the time clock where the time off will be presented in
    the timesheet
    """


class V1CreateRequestResponse(BaseModel):
    data: Data

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
