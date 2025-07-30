# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from ....._utils import PropertyInfo
from .shift_break_type import ShiftBreakType
from .location_data_param import LocationDataParam
from .html_note_data_param import HTMLNoteDataParam

__all__ = ["ShiftUpdateParams", "Body", "BodyBreak"]


class ShiftUpdateParams(TypedDict, total=False):
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

    id: str
    """The unique identifier of the break.

    If this field is left empty, a new break will be created
    """

    start_time: Annotated[int, PropertyInfo(alias="startTime")]
    """The time the break starts, counted in minutes from the beginning of the day"""


class Body(TypedDict, total=False):
    shift_id: Required[Annotated[str, PropertyInfo(alias="shiftId")]]
    """The unique identifier of the shift"""

    assigned_user_ids: Annotated[Iterable[int], PropertyInfo(alias="assignedUserIds")]
    """The list of assigned user IDs for the shift.

    Currently, only one user ID can be specified.
    """

    breaks: Iterable[BodyBreak]
    """The list of breaks for the shift"""

    color: str
    """The color associated with the shift.

    Should be one of the following colors: ['#4B7AC5', '#801A1A', '#AE2121',
    '#DC7A7A', '#B0712E', '#D4985A', '#E4B37F', '#AE8E2D', '#CBA73A', '#D9B443',
    '#487037', '#6F9B5C', '#91B282', '#365C64', '#5687B3', '#7C9BA2', '#3968BB',
    '#85A6DA', '#225A8C', '#548CBE', '#81A8CC', '#4E3F75', '#604E8E', '#8679AA',
    '#983D73', '#A43778', '#D178AD', '#6B2E4C', '#925071', '#B57D9A', '#3a3a3a',
    '#616161', '#969696']
    """

    end_time: Annotated[int, PropertyInfo(alias="endTime")]
    """The end time of the shift in Unix format (in seconds)"""

    is_edit_for_all_users: Annotated[bool, PropertyInfo(alias="isEditForAllUsers")]
    """
    Indicates whether the update should be applied to all users assigned to the
    shift
    """

    is_open_shift: Annotated[bool, PropertyInfo(alias="isOpenShift")]
    """Indicates whether the shift is an open shift. Creates only with 1 open spot"""

    is_published: Annotated[bool, PropertyInfo(alias="isPublished")]
    """Indicates whether the shift is published"""

    is_require_admin_approval: Annotated[bool, PropertyInfo(alias="isRequireAdminApproval")]
    """Indicates whether admin approval is required for the shift.

    Can only be set if the shift is an open shift
    """

    job_id: Annotated[str, PropertyInfo(alias="jobId")]
    """The ID of the associated job"""

    location_data: Annotated[LocationDataParam, PropertyInfo(alias="locationData")]
    """The location data for the shift"""

    notes: Iterable[HTMLNoteDataParam]
    """Additional notes for the shift"""

    start_time: Annotated[int, PropertyInfo(alias="startTime")]
    """The start time of the shift in Unix format (in seconds)"""

    timezone: str
    """The timezone in Tz format (e.g. America/New_York)"""

    title: str
    """The title of the shift"""
