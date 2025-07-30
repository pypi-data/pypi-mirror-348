# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel
from .assign_data_types import AssignDataTypes
from ...time_clock.v1.gps_data import GpsData

__all__ = ["BaseJobResponse", "Assign"]


class Assign(BaseModel):
    type: AssignDataTypes
    """An enumeration."""

    group_ids: Optional[List[int]] = FieldInfo(alias="groupIds", default=None)
    """The group ids to assign to this entity (if assigning type is groups)."""

    user_ids: Optional[List[int]] = FieldInfo(alias="userIds", default=None)
    """The user ids to assign to this entity (if assigning type is users)."""


class BaseJobResponse(BaseModel):
    assign: Assign
    """Data related to job assignment"""

    code: str
    """The code of the Job."""

    color: str
    """The color associated with the job"""

    description: str
    """The job description"""

    job_id: str = FieldInfo(alias="jobId")
    """The job ID"""

    title: str
    """The title of the Job"""

    gps: Optional[GpsData] = None
    """GPS data associated with the job"""

    instance_ids: Optional[List[int]] = FieldInfo(alias="instanceIds", default=None)
    """The instance IDs associated with the job"""

    is_deleted: Optional[bool] = FieldInfo(alias="isDeleted", default=None)
    """Indicates whether the job is deleted or not"""

    parent_id: Optional[str] = FieldInfo(alias="parentId", default=None)
    """The ID of the parent job, if any"""

    sub_jobs: Optional[List[object]] = FieldInfo(alias="subJobs", default=None)
    """The sub jobs of the parent job, if any"""

    use_parent_data: Optional[bool] = FieldInfo(alias="useParentData", default=None)
    """Indicates whether to use the parent job's data or not"""
