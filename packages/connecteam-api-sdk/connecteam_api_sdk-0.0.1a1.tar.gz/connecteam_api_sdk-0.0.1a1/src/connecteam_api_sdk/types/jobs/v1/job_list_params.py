# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal, Annotated, TypedDict

from ...._utils import PropertyInfo
from ...scheduler.v1.schedulers.sort_order import SortOrder

__all__ = ["JobListParams"]


class JobListParams(TypedDict, total=False):
    include_deleted: Annotated[bool, PropertyInfo(alias="includeDeleted")]
    """Determines whether the response includes jobs that have been deleted.

    Default value is set to true.
    """

    instance_ids: Annotated[Iterable[int], PropertyInfo(alias="instanceIds")]
    """List of instance IDs (scheduler id or time clock id) to filter by"""

    job_codes: Annotated[List[str], PropertyInfo(alias="jobCodes")]
    """List of job codes to filter by.

    In case where a sub-job code is provided, the relevant sub-job with all other
    nested sub-jobs will be retrieved alongside with the parent job.
    """

    job_ids: Annotated[List[str], PropertyInfo(alias="jobIds")]
    """List of job IDs to filter by.

    In cases where a job ID includes nested sub-jobs, all sub-jobs under that parent
    job will be retrieved alongside with the parent job. Note that this filter does
    not support direct querying by sub-job IDs. To retrieve specific sub-jobs,
    please use the Get Job endpoint
    """

    job_names: Annotated[List[str], PropertyInfo(alias="jobNames")]
    """List of job names to filter by.

    In case where a sub-job name is provided, the relevant sub-job with all other
    nested sub-jobs will be retrieved alongside with the parent job.
    """

    limit: int
    """The maximum number of results to display per page"""

    offset: int
    """
    The resource offset of the last successfully read resource will be returned as
    the paging.offset JSON property of a paginated response containing more results
    """

    order: SortOrder
    """An enumeration."""

    sort: Literal["title"]
    """An enumeration."""
