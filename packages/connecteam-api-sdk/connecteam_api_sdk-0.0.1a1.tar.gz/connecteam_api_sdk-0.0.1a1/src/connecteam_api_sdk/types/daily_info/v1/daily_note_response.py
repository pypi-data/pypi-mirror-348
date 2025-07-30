# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["DailyNoteResponse", "Data"]


class Data(BaseModel):
    id: int
    """The note ID"""

    dates: List[str]
    """Dates the note is relevant for in ISO 8601 format (e.g. YYYY-MM-DD)"""

    title: str
    """The title of the note"""

    qualified_group_ids: Optional[List[int]] = FieldInfo(alias="qualifiedGroupIds", default=None)
    """The groups qualified to see the note"""

    qualified_user_ids: Optional[List[int]] = FieldInfo(alias="qualifiedUserIds", default=None)
    """The users qualified to see the note"""


class DailyNoteResponse(BaseModel):
    data: Data

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
