# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["TimeClockListResponse", "Data", "DataTimeClock"]


class DataTimeClock(BaseModel):
    id: int
    """The ID of the time clock"""

    is_archived: bool = FieldInfo(alias="isArchived")
    """Whether the time clock is archived"""

    name: str
    """The name of the time clock"""


class Data(BaseModel):
    time_clocks: List[DataTimeClock] = FieldInfo(alias="timeClocks")
    """The time clocks"""


class TimeClockListResponse(BaseModel):
    data: Data

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
