# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo
from .gps_data_param import GpsDataParam

__all__ = ["TimeClockClockInParams"]


class TimeClockClockInParams(TypedDict, total=False):
    job_id: Required[Annotated[str, PropertyInfo(alias="jobId")]]
    """The unique identifier of the associated job or sub-job.

    Make sure the job is assigned to the specified time clock.
    """

    user_id: Required[Annotated[int, PropertyInfo(alias="userId")]]
    """The unique identifier of the user.

    Make sure the user is assigned to the specified time clock.
    """

    location_data: Annotated[GpsDataParam, PropertyInfo(alias="locationData")]
    """GPS data associated with the clocking in event"""

    scheduler_shift_id: Annotated[str, PropertyInfo(alias="schedulerShiftId")]
    """
    The scheduled shift from the job scheduler associated with the clocking in event
    """

    timezone: str
    """The timezone in Tz format (e.g.

    America/New_York). If timezone is not specified, it will use the default
    timezone in the time clock settings.
    """
