# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ...._models import BaseModel

__all__ = ["TimestampWithTimezoneScheduler"]


class TimestampWithTimezoneScheduler(BaseModel):
    timestamp: int
    """The timestamp in Unix format (in seconds)"""

    timezone: str
    """The timezone in Tz format (e.g. America/New_York)"""
