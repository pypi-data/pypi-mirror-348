# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Required, Annotated, TypedDict

from .task_type import TaskType
from ....._utils import PropertyInfo
from .task_status import TaskStatus
from .task_description_param import TaskDescriptionParam

__all__ = ["TaskCreateParams"]


class TaskCreateParams(TypedDict, total=False):
    due_date: Required[Annotated[int, PropertyInfo(alias="dueDate")]]
    """The due date of the task in Unix format (in seconds)"""

    start_time: Required[Annotated[int, PropertyInfo(alias="startTime")]]
    """The start time of the task in Unix format (in seconds)"""

    status: Required[TaskStatus]
    """An enumeration."""

    title: Required[str]
    """The title of the task"""

    user_ids: Required[Annotated[Iterable[int], PropertyInfo(alias="userIds")]]
    """List of user IDs to assign the task to.

    If more than one user ID is specified, it will be treated as a group task. To
    assign the task to multiple users individually, separate the requests. If this
    field remains empty the status field must be 'draft' and not archived.
    """

    description: TaskDescriptionParam
    """Specifies additional description on the task"""

    is_archived: Annotated[bool, PropertyInfo(alias="isArchived")]
    """Indicates if the task is archived"""

    label_ids: Annotated[List[str], PropertyInfo(alias="labelIds")]
    """List of labels IDs associated with the task"""

    type: TaskType
    """An enumeration."""
