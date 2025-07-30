# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo
from .gps_data_param import GpsDataParam

__all__ = ["TimeClockClockOutParams"]


class TimeClockClockOutParams(TypedDict, total=False):
    user_id: Required[Annotated[int, PropertyInfo(alias="userId")]]
    """The unique identifier of the user.

    Make sure the user is assigned to the specified time clock.
    """

    location_data: Annotated[GpsDataParam, PropertyInfo(alias="locationData")]
    """GPS data associated with the clocking out event"""

    timezone: str
    """The timezone in Tz format (e.g.

    America/New_York). If timezone is not specified, it will use the default
    timezone in the time clock settings.
    """
