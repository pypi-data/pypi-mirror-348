# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ....._utils import PropertyInfo
from ....time_clock.v1.gps_data_param import GpsDataParam

__all__ = ["LocationDataParam"]


class LocationDataParam(TypedDict, total=False):
    is_referenced_to_job: Required[Annotated[bool, PropertyInfo(alias="isReferencedToJob")]]
    """Indicates whether the location is referenced to a job.

    can only be true if job id isn't empty
    """

    gps: GpsDataParam
    """GPS data associated with the location."""
