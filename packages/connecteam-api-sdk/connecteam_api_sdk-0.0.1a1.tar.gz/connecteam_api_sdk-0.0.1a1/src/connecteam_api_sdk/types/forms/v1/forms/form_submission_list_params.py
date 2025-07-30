# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["FormSubmissionListParams"]


class FormSubmissionListParams(TypedDict, total=False):
    limit: int
    """The maximum number of results to display per page"""

    offset: int
    """
    The resource offset of the last successfully read resource will be returned as
    the paging.offset JSON property of a paginated response containing more results
    """

    submitting_end_time: Annotated[int, PropertyInfo(alias="submittingEndTime")]
    """Filter form submissions that were submitted until this timestamp"""

    submitting_start_timestamp: Annotated[int, PropertyInfo(alias="submittingStartTimestamp")]
    """Filter form submissions that were submitted from this timestamp"""

    user_ids: Annotated[Iterable[int], PropertyInfo(alias="userIds")]
    """Filter by submitting user ids"""
