# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from ....._utils import PropertyInfo
from .shift_break_type import ShiftBreakType
from .location_data_param import LocationDataParam
from .html_note_data_param import HTMLNoteDataParam
from ....time_clock.v1.gps_data_param import GpsDataParam

__all__ = [
    "ShiftCreateParams",
    "Body",
    "BodyBreak",
    "BodyShiftDetails",
    "BodyShiftDetailsShiftLayer",
    "BodyShiftDetailsShiftLayerValue",
    "BodyStatus",
]


class ShiftCreateParams(TypedDict, total=False):
    body: Required[Iterable[Body]]

    notify_users: Annotated[bool, PropertyInfo(alias="notifyUsers")]
    """Indicates whether to send a notification to the users assigned to the shifts.

    This applies only to shifts that are published.
    """


class BodyBreak(TypedDict, total=False):
    duration: Required[int]
    """The time the break lasts in minutes"""

    name: Required[str]
    """The name of the break."""

    type: Required[ShiftBreakType]
    """An enumeration."""

    start_time: Annotated[int, PropertyInfo(alias="startTime")]
    """The time the break starts, counted in minutes from the beginning of the day"""


class BodyShiftDetailsShiftLayerValue(TypedDict, total=False):
    id: Required[str]
    """The unique identifier of the value"""


class BodyShiftDetailsShiftLayer(TypedDict, total=False):
    id: Required[str]
    """The unique identifier of the shift layer"""

    value: Required[BodyShiftDetailsShiftLayerValue]
    """The value of the shift layer"""


class BodyShiftDetails(TypedDict, total=False):
    shift_layers: Annotated[Iterable[BodyShiftDetailsShiftLayer], PropertyInfo(alias="shiftLayers")]
    """The various layers of information associated with the shift"""

    shift_source: Annotated[str, PropertyInfo(alias="shiftSource")]
    """The source of the shift"""


class BodyStatus(TypedDict, total=False):
    gps: GpsDataParam
    """The GPS data of the status"""

    note: str
    """The note of the status"""

    should_override_previous_statuses: Annotated[bool, PropertyInfo(alias="shouldOverridePreviousStatuses")]
    """Indicates whether to override previous statuses"""


class Body(TypedDict, total=False):
    end_time: Required[Annotated[int, PropertyInfo(alias="endTime")]]
    """The end time of the shift in Unix format (in seconds)"""

    start_time: Required[Annotated[int, PropertyInfo(alias="startTime")]]
    """The start time of the shift in Unix format (in seconds)"""

    assigned_user_ids: Annotated[Iterable[int], PropertyInfo(alias="assignedUserIds")]
    """The list of assigned user IDs for the shift.

    Currently, only one user ID can be specified. If the shift is open, this list
    should remain empty.
    """

    breaks: Iterable[BodyBreak]
    """A list of breaks to create for the shift"""

    color: str
    """
    The color associated with the shift, defaults to the color of the job linked to
    the shift. If a specific color is provided, it will override the default job
    color. Defaults to #4B7AC5. Should be one of the following colors: ['#4B7AC5',
    '#801A1A', '#AE2121', '#DC7A7A', '#B0712E', '#D4985A', '#E4B37F', '#AE8E2D',
    '#CBA73A', '#D9B443', '#487037', '#6F9B5C', '#91B282', '#365C64', '#5687B3',
    '#7C9BA2', '#3968BB', '#85A6DA', '#225A8C', '#548CBE', '#81A8CC', '#4E3F75',
    '#604E8E', '#8679AA', '#983D73', '#A43778', '#D178AD', '#6B2E4C', '#925071',
    '#B57D9A', '#3a3a3a', '#616161', '#969696']
    """

    is_open_shift: Annotated[bool, PropertyInfo(alias="isOpenShift")]
    """Indicates whether the shift is an open shift. Creates only with 1 open spot"""

    is_published: Annotated[bool, PropertyInfo(alias="isPublished")]
    """Indicates whether the shift is published"""

    is_require_admin_approval: Annotated[bool, PropertyInfo(alias="isRequireAdminApproval")]
    """Indicates whether admin approval is required for claiming the shift.

    Can only be set if the shift is an open shift
    """

    job_id: Annotated[str, PropertyInfo(alias="jobId")]
    """The ID of the associated job"""

    location_data: Annotated[LocationDataParam, PropertyInfo(alias="locationData")]
    """The location data for the shift"""

    notes: Iterable[HTMLNoteDataParam]
    """Additional notes for the shift"""

    shift_details: Annotated[BodyShiftDetails, PropertyInfo(alias="shiftDetails")]
    """The additional details on the shift, if applicable."""

    statuses: Iterable[BodyStatus]
    """The list of statuses associated with the shift"""

    timezone: str
    """The timezone of the shift in Tz format (e.g.

    America/New_York). If not specified, it uses the timezone configured in the app
    settings
    """

    title: str
    """
    The title of the shift, If this field remains empty, the jobId field must be
    specified.
    """
