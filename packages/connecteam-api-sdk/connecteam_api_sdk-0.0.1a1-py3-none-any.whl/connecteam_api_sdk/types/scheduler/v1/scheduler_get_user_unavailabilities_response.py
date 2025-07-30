# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ...._models import BaseModel
from .timestamp_with_timezone_scheduler import TimestampWithTimezoneScheduler

__all__ = [
    "SchedulerGetUserUnavailabilitiesResponse",
    "Data",
    "DataUserUnavailability",
    "DataUserUnavailabilityShift",
    "DataUserUnavailabilityUnavailability",
]


class DataUserUnavailabilityShift(BaseModel):
    id: str
    """The unique identifier of the shift"""

    end_time: TimestampWithTimezoneScheduler = FieldInfo(alias="endTime")
    """The end time of the shift"""

    instance_id: int = FieldInfo(alias="instanceId")
    """The unique identifier of the scheduler instance"""

    start_time: TimestampWithTimezoneScheduler = FieldInfo(alias="startTime")
    """The start time of the shift"""


class DataUserUnavailabilityUnavailability(BaseModel):
    end_time: TimestampWithTimezoneScheduler = FieldInfo(alias="endTime")
    """The end time of the unavailability"""

    note: str
    """The note of the unavailability"""

    start_time: TimestampWithTimezoneScheduler = FieldInfo(alias="startTime")
    """The start time of the unavailability"""

    type: Literal["unavailability", "timeOff"]
    """An enumeration."""

    id: Optional[str] = None
    """The unique identifier of the unavailability"""

    instance_id: Optional[int] = FieldInfo(alias="instanceId", default=None)
    """
    The scheduler id of the unavailability (applicable only when unavailability type
    is unavailability)
    """

    policy_name: Optional[str] = FieldInfo(alias="policyName", default=None)
    """The name of the policy (applicable only when unavailability type is timeOff)"""


class DataUserUnavailability(BaseModel):
    shifts: List[DataUserUnavailabilityShift]
    """List of assigned shifts"""

    unavailabilities: List[DataUserUnavailabilityUnavailability]
    """List of approved unavailabilities"""

    user_id: int = FieldInfo(alias="userId")
    """The unique identifier of the user"""


class Data(BaseModel):
    user_unavailabilities: List[DataUserUnavailability] = FieldInfo(alias="userUnavailabilities")
    """List of users with unavailabilities"""


class SchedulerGetUserUnavailabilitiesResponse(BaseModel):
    data: Data

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
