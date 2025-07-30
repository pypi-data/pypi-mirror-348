# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .task_type import TaskType
from ....._models import BaseModel
from .task_status import TaskStatus
from ....settings.v1.paging_response import PagingResponse

__all__ = ["TaskListResponse", "Data", "DataTask"]


class DataTask(BaseModel):
    id: str
    """The unique identifier of the task"""

    due_date: int = FieldInfo(alias="dueDate")
    """The due date of the task in Unix format (in seconds)"""

    start_time: int = FieldInfo(alias="startTime")
    """The start time of the task in Unix format (in seconds)"""

    status: TaskStatus
    """An enumeration."""

    title: str
    """The title of the task"""

    user_ids: List[int] = FieldInfo(alias="userIds")
    """List of user IDs to assign the task to.

    If more than one user ID is specified, it will be treated as a group task. To
    assign the task to multiple users individually, separate the requests. If this
    field remains empty the status field must be 'draft' and not archived.
    """

    is_archived: Optional[bool] = FieldInfo(alias="isArchived", default=None)
    """Indicates if the task is archived"""

    label_ids: Optional[List[str]] = FieldInfo(alias="labelIds", default=None)
    """List of labels IDs associated with the task"""

    type: Optional[TaskType] = None
    """An enumeration."""


class Data(BaseModel):
    tasks: List[DataTask]
    """List of tasks"""


class TaskListResponse(BaseModel):
    data: Data

    paging: PagingResponse

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
