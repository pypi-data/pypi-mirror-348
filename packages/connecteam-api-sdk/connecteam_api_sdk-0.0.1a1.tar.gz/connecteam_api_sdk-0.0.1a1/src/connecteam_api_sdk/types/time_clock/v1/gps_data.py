# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ...._models import BaseModel

__all__ = ["GpsData"]


class GpsData(BaseModel):
    address: Optional[str] = None
    """The address associated with the GPS data."""

    latitude: Optional[float] = None
    """The latitude coordinate."""

    longitude: Optional[float] = None
    """The longitude coordinate."""
