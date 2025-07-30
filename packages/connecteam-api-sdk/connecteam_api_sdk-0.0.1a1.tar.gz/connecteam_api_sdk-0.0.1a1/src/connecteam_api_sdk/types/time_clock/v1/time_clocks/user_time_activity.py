# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ....._models import BaseModel
from ..time_activity_time_point import TimeActivityTimePoint

__all__ = [
    "UserTimeActivity",
    "ManualBreak",
    "Shift",
    "ShiftShiftAttachment",
    "ShiftShiftAttachmentAttachment",
    "ShiftShiftAttachmentAttachmentFile",
    "TimeOff",
    "TimeOffDuration",
]


class ManualBreak(BaseModel):
    id: str
    """The unique identifier of the time clock"""

    manual_break_id: str = FieldInfo(alias="manualBreakId")
    """The ID of the manual break"""

    start: TimeActivityTimePoint
    """The start time of the time activity"""

    created_at: Optional[int] = FieldInfo(alias="createdAt", default=None)
    """The creation time of the time activity"""

    employee_note: Optional[str] = FieldInfo(alias="employeeNote", default=None)
    """The employee note providing additional details"""

    end: Optional[TimeActivityTimePoint] = None
    """The end time of the time activity"""

    is_auto_clock_out: Optional[bool] = FieldInfo(alias="isAutoClockOut", default=None)
    """Indicates whether the user was auto clocked out from the shift"""

    manager_note: Optional[str] = FieldInfo(alias="managerNote", default=None)
    """The manager note providing additional details"""

    modified_at: Optional[int] = FieldInfo(alias="modifiedAt", default=None)
    """The last modification time of the time activity"""


class ShiftShiftAttachmentAttachmentFile(BaseModel):
    file_name: str = FieldInfo(alias="fileName")
    """The name of the file in a shift attachment of type file"""

    file_url: str = FieldInfo(alias="fileUrl")
    """The URL of the file in a shift attachment of type file"""


class ShiftShiftAttachmentAttachment(BaseModel):
    file_name: Optional[str] = FieldInfo(alias="fileName", default=None)
    """The name of the file in a shift attachment of type file"""

    files: Optional[List[ShiftShiftAttachmentAttachmentFile]] = None
    """The value of the shift attachment of type files"""

    file_url: Optional[str] = FieldInfo(alias="fileUrl", default=None)
    """The URL of the file in a shift attachment of type file"""

    free_text: Optional[str] = FieldInfo(alias="freeText", default=None)
    """The value of the shift attachment of type free text"""

    image: Optional[str] = None
    """The value of the shift attachment of type signature"""

    images: Optional[List[str]] = None
    """The value of the shift attachment of type images"""

    item_id: Optional[str] = FieldInfo(alias="itemId", default=None)
    """The ID of the dropdown list item"""

    number: Optional[float] = None
    """The value of the shift attachment of type number"""


class ShiftShiftAttachment(BaseModel):
    attachment: ShiftShiftAttachmentAttachment
    """The value of the shift attachment"""

    shift_attachment_id: str = FieldInfo(alias="shiftAttachmentId")
    """The ID of the shift attachment"""


class Shift(BaseModel):
    id: str
    """The unique identifier of the time clock"""

    job_id: str = FieldInfo(alias="jobId")
    """The ID of the job"""

    start: TimeActivityTimePoint
    """The start time of the time activity"""

    created_at: Optional[int] = FieldInfo(alias="createdAt", default=None)
    """The creation time of the time activity"""

    employee_note: Optional[str] = FieldInfo(alias="employeeNote", default=None)
    """The employee note providing additional details"""

    end: Optional[TimeActivityTimePoint] = None
    """The end time of the time activity"""

    is_auto_clock_out: Optional[bool] = FieldInfo(alias="isAutoClockOut", default=None)
    """Indicates whether the user was auto clocked out from the shift"""

    manager_note: Optional[str] = FieldInfo(alias="managerNote", default=None)
    """The manager note providing additional details"""

    modified_at: Optional[int] = FieldInfo(alias="modifiedAt", default=None)
    """The last modification time of the time activity"""

    scheduler_shift_id: Optional[str] = FieldInfo(alias="schedulerShiftId", default=None)
    """The unique identifier of the shift from the job scheduler, if it exists."""

    shift_attachments: Optional[List[ShiftShiftAttachment]] = FieldInfo(alias="shiftAttachments", default=None)
    """The shift attachments"""

    sub_job_id: Optional[str] = FieldInfo(alias="subJobId", default=None)
    """The ID of the sub job"""


class TimeOffDuration(BaseModel):
    units: Literal["hours", "days"]
    """An enumeration."""

    value: float
    """The value of the duration"""


class TimeOff(BaseModel):
    id: str
    """The unique identifier of the time clock"""

    duration: TimeOffDuration
    """The duration of the time off"""

    is_all_day: bool = FieldInfo(alias="isAllDay")
    """Indicates whether the time off is all day"""

    policy_type_id: str = FieldInfo(alias="policyTypeId")
    """The ID of the policy type"""

    start: TimeActivityTimePoint
    """The start time of the time activity"""

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


class UserTimeActivity(BaseModel):
    manual_breaks: List[ManualBreak] = FieldInfo(alias="manualBreaks")
    """The manual breaks"""

    shifts: List[Shift]
    """The shifts"""

    user_id: int = FieldInfo(alias="userId")
    """The ID of the user"""

    time_offs: Optional[List[TimeOff]] = FieldInfo(alias="timeOffs", default=None)
    """The time offs"""
