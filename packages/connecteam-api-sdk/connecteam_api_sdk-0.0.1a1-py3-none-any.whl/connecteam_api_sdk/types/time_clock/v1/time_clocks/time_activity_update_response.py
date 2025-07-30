# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ....._models import BaseModel
from .user_time_activity import UserTimeActivity

__all__ = ["TimeActivityUpdateResponse", "Data"]


class Data(BaseModel):
    time_activities_by_users: List[UserTimeActivity] = FieldInfo(alias="timeActivitiesByUsers")
    """The time activities"""


class TimeActivityUpdateResponse(BaseModel):
    data: Data

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
