# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["TaskboardListResponse", "Data", "DataTaskBoard"]


class DataTaskBoard(BaseModel):
    id: int
    """The ID of the tasks board"""

    is_archived: bool = FieldInfo(alias="isArchived")
    """Whether the tasks board is archived"""

    name: str
    """The name of the tasks board"""


class Data(BaseModel):
    task_boards: List[DataTaskBoard] = FieldInfo(alias="taskBoards")
    """All tasks boards in your account"""


class TaskboardListResponse(BaseModel):
    data: Data

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
