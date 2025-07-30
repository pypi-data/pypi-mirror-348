# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal, Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["TaskListParams"]


class TaskListParams(TypedDict, total=False):
    label_ids: Annotated[List[str], PropertyInfo(alias="labelIds")]
    """List of label IDs to filter by.

    Tasks retrieved will include the specified label(s), but may also include
    additional labels.
    """

    limit: int
    """The maximum number of results to display per page"""

    offset: int
    """
    The resource offset of the last successfully read resource will be returned as
    the paging.offset JSON property of a paginated response containing more results
    """

    status: Literal["draft", "published", "completed", "all"]
    """An enumeration."""

    task_ids: Annotated[List[str], PropertyInfo(alias="taskIds")]
    """List of task IDs to filter by"""

    user_ids: Annotated[Iterable[int], PropertyInfo(alias="userIds")]
    """List of assigned user IDs on the task to filter by.

    Group tasks will be also included in the results.
    """
