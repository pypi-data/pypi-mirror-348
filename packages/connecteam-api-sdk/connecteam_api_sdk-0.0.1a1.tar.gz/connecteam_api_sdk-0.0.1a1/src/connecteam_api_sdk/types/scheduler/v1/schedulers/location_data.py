# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ....._models import BaseModel
from ....time_clock.v1.gps_data import GpsData

__all__ = ["LocationData"]


class LocationData(BaseModel):
    is_referenced_to_job: bool = FieldInfo(alias="isReferencedToJob")
    """Indicates whether the location is referenced to a job.

    can only be true if job id isn't empty
    """

    gps: Optional[GpsData] = None
    """GPS data associated with the location."""
