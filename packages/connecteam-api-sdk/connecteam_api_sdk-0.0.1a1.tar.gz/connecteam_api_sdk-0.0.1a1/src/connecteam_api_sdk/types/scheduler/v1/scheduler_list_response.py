# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["SchedulerListResponse", "Data", "DataScheduler"]


class DataScheduler(BaseModel):
    is_archived: bool = FieldInfo(alias="isArchived")
    """Indicates whether the scheduler is archived"""

    name: str
    """The name of the scheduler"""

    scheduler_id: int = FieldInfo(alias="schedulerId")
    """The unique identifier of the scheduler"""

    timezone: str
    """The timezone of the scheduler in Tz format"""


class Data(BaseModel):
    schedulers: List[DataScheduler]
    """The schedulers"""


class SchedulerListResponse(BaseModel):
    data: Data

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
