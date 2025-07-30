# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .gps_data import GpsData
from ...._models import BaseModel

__all__ = ["TimeActivityTimePoint"]


class TimeActivityTimePoint(BaseModel):
    timestamp: int
    """The timestamp in Unix format (in seconds)"""

    timezone: str
    """The timezone in Tz format (e.g. America/New_York)"""

    location_data: Optional[GpsData] = FieldInfo(alias="locationData", default=None)
    """The location data"""
