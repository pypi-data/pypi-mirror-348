# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["TimeClockGetManualBreaksResponse", "Data", "DataManualBreak"]


class DataManualBreak(BaseModel):
    id: str
    """The ID of the manual break"""

    duration: int
    """The duration of the manual break in minutes"""

    is_paid: bool = FieldInfo(alias="isPaid")
    """Whether the manual break is paid"""

    name: str
    """The name of the manual break"""


class Data(BaseModel):
    are_manual_breaks_enabled: bool = FieldInfo(alias="areManualBreaksEnabled")
    """Whether manual breaks are enabled"""

    manual_breaks: List[DataManualBreak] = FieldInfo(alias="manualBreaks")
    """The manual breaks"""


class TimeClockGetManualBreaksResponse(BaseModel):
    data: Data

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
