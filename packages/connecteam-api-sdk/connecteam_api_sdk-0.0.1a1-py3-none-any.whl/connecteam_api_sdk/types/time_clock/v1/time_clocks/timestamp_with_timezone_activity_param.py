# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["TimestampWithTimezoneActivityParam"]


class TimestampWithTimezoneActivityParam(TypedDict, total=False):
    timestamp: Required[int]
    """The timestamp in Unix format (in seconds)"""

    timezone: Required[str]
    """The timezone in Tz format (e.g. America/New_York)"""
