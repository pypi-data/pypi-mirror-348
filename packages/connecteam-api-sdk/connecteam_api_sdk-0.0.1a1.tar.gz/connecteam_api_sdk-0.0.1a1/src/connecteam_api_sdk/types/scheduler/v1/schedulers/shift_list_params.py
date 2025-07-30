# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from ....._utils import PropertyInfo
from .sort_order import SortOrder

__all__ = ["ShiftListParams"]


class ShiftListParams(TypedDict, total=False):
    end_time: Required[Annotated[int, PropertyInfo(alias="endTime")]]
    """The end time to filter by in Unix format (in seconds)"""

    start_time: Required[Annotated[int, PropertyInfo(alias="startTime")]]
    """The start time to filter by in Unix format (in seconds)"""

    assigned_user_ids: Annotated[Iterable[int], PropertyInfo(alias="assignedUserIds")]
    """List of user IDs"""

    is_open_shift: Annotated[bool, PropertyInfo(alias="isOpenShift")]
    """Filter shifts that are open shifts"""

    is_published: Annotated[bool, PropertyInfo(alias="isPublished")]
    """Filter shifts that are published"""

    is_require_admin_approval: Annotated[bool, PropertyInfo(alias="isRequireAdminApproval")]
    """Filter shifts that require admin approval"""

    job_id: Annotated[List[str], PropertyInfo(alias="jobId")]
    """List of job IDs"""

    limit: int
    """The maximum number of results to display per page"""

    offset: int
    """
    The resource offset of the last successfully read resource will be returned as
    the paging.offset JSON property of a paginated response containing more results
    """

    order: SortOrder
    """An enumeration."""

    shift_id: Annotated[List[str], PropertyInfo(alias="shiftId")]
    """List of shift IDs"""

    sort: Literal["created_at", "updated_at"]
    """An enumeration."""

    title: str
    """Title of the shift"""
