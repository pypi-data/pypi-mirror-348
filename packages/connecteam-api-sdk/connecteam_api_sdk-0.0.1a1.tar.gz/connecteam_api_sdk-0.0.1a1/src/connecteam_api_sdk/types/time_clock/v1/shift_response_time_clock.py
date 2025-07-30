# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel
from .time_activity_time_point import TimeActivityTimePoint

__all__ = ["ShiftResponseTimeClock"]


class ShiftResponseTimeClock(BaseModel):
    id: str
    """The unique identifier of the time clock"""

    job_id: str = FieldInfo(alias="jobId")
    """The unique identifier of the associated job or sub-job.

    Make sure the job is assigned to the specified time clock.
    """

    start: TimeActivityTimePoint
    """The start time of the time activity"""

    user_id: int = FieldInfo(alias="userId")
    """The unique identifier of the user.

    Make sure the user is assigned to the specified time clock.
    """

    created_at: Optional[int] = FieldInfo(alias="createdAt", default=None)
    """The creation time of the time activity"""

    employee_note: Optional[str] = FieldInfo(alias="employeeNote", default=None)
    """The employee note providing additional details"""

    end: Optional[TimeActivityTimePoint] = None
    """The end time of the time activity"""

    manager_note: Optional[str] = FieldInfo(alias="managerNote", default=None)
    """The manager note providing additional details"""

    modified_at: Optional[int] = FieldInfo(alias="modifiedAt", default=None)
    """The last modification time of the time activity"""

    scheduler_shift_id: Optional[str] = FieldInfo(alias="schedulerShiftId", default=None)
    """
    The scheduled shift from the job scheduler associated with the clocking in event
    """
