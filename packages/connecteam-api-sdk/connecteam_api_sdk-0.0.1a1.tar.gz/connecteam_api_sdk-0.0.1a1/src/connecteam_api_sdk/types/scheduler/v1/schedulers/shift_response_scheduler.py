# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from ....._models import BaseModel
from .location_data import LocationData
from .shift_break_type import ShiftBreakType
from ....time_clock.v1.gps_data import GpsData

__all__ = [
    "ShiftResponseScheduler",
    "ShiftDetails",
    "ShiftDetailsShiftLayer",
    "ShiftDetailsShiftLayerValue",
    "Break",
    "Note",
    "NoteHTMLNoteDataOut",
    "NoteAlbumNoteDataOut",
    "NoteAlbumNoteDataOutAlbum",
    "NoteFileNoteDataOut",
    "Status",
]


class ShiftDetailsShiftLayerValue(BaseModel):
    id: str
    """The unique identifier of the value"""

    display_name: str = FieldInfo(alias="displayName")
    """The name of the value"""


class ShiftDetailsShiftLayer(BaseModel):
    id: str
    """The unique identifier of the shift layer"""

    title: str
    """The name of the shift layer"""

    value: ShiftDetailsShiftLayerValue
    """The value of the shift layer"""


class ShiftDetails(BaseModel):
    shift_layers: Optional[List[ShiftDetailsShiftLayer]] = FieldInfo(alias="shiftLayers", default=None)
    """The various layers of information associated with the shift"""

    shift_source: Optional[str] = FieldInfo(alias="shiftSource", default=None)
    """The source of the shift"""


class Break(BaseModel):
    id: str
    """The id of the break"""

    duration: int
    """The time the break lasts in minutes"""

    name: str
    """The name of the break."""

    type: ShiftBreakType
    """An enumeration."""

    start_time: Optional[int] = FieldInfo(alias="startTime", default=None)
    """The time the break starts, counted in minutes from the beginning of the day"""


class NoteHTMLNoteDataOut(BaseModel):
    html: str
    """The HTML content of the note"""

    type: Optional[str] = None
    """HTML note type"""


class NoteAlbumNoteDataOutAlbum(BaseModel):
    url: str
    """The url of the file to upload"""


class NoteAlbumNoteDataOut(BaseModel):
    album: List[NoteAlbumNoteDataOutAlbum]
    """The list of images in the album"""

    type: Optional[str] = None
    """Album note type"""


class NoteFileNoteDataOut(BaseModel):
    name: str
    """The name of the file"""

    url: str
    """The url of the file to upload"""

    type: Optional[str] = None
    """URL note type"""


Note: TypeAlias = Union[NoteHTMLNoteDataOut, NoteAlbumNoteDataOut, NoteFileNoteDataOut]


class Status(BaseModel):
    creating_user_id: int = FieldInfo(alias="creatingUserId")
    """The ID of the user who created the status"""

    creation_time: int = FieldInfo(alias="creationTime")
    """The creation time of the status"""

    status: Literal[
        "accepted",
        "checked_in",
        "completed",
        "rejected",
        "claimed",
        "claim_requested",
        "unclaimed",
        "unclaim_requested",
        "cancel_claim_request",
        "reset",
    ]
    """An enumeration."""

    status_id: str = FieldInfo(alias="statusId")
    """The ID of the status"""

    attachments: Optional[List[str]] = None
    """The attachments of the status"""

    gps: Optional[GpsData] = None
    """The GPS data of the status"""

    modifying_user_id: Optional[int] = FieldInfo(alias="modifyingUserId", default=None)
    """The ID of the user who modified the status"""

    note: Optional[str] = None
    """The note of the status"""

    update_time: Optional[int] = FieldInfo(alias="updateTime", default=None)
    """The update time of the status"""


class ShiftResponseScheduler(BaseModel):
    id: str
    """The ID of the shift"""

    color: str
    """The color of the shift"""

    end_time: int = FieldInfo(alias="endTime")
    """The end time of the shift"""

    is_open_shift: bool = FieldInfo(alias="isOpenShift")
    """Whether the shift is an open shift"""

    is_published: bool = FieldInfo(alias="isPublished")
    """Whether the shift is published"""

    shift_details: ShiftDetails = FieldInfo(alias="shiftDetails")
    """The additional details on the shift, if applicable"""

    start_time: int = FieldInfo(alias="startTime")
    """The start time of the shift"""

    timezone: str
    """The timezone of the shift"""

    title: str
    """The title of the shift"""

    assigned_user_ids: Optional[List[int]] = FieldInfo(alias="assignedUserIds", default=None)
    """The IDs of the assigned users"""

    breaks: Optional[List[Break]] = None
    """The breaks of the shift"""

    creation_time: Optional[int] = FieldInfo(alias="creationTime", default=None)
    """The creation time of the shift"""

    is_require_admin_approval: Optional[bool] = FieldInfo(alias="isRequireAdminApproval", default=None)
    """Whether the shift requires admin approval"""

    job_id: Optional[str] = FieldInfo(alias="jobId", default=None)
    """The ID of the job"""

    location_data: Optional[LocationData] = FieldInfo(alias="locationData", default=None)
    """The location data"""

    notes: Optional[List[Note]] = None
    """The notes of the shift"""

    open_spots: Optional[int] = FieldInfo(alias="openSpots", default=None)
    """The number of open spots"""

    statuses: Optional[List[Status]] = None
    """The statuses of the shift"""

    update_time: Optional[int] = FieldInfo(alias="updateTime", default=None)
    """The update time of the shift"""
