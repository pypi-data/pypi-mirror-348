# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["GpsDataParam"]


class GpsDataParam(TypedDict, total=False):
    address: str
    """The address associated with the GPS data."""

    latitude: float
    """The latitude coordinate."""

    longitude: float
    """The longitude coordinate."""
