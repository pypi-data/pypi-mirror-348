# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["V1GetSmartGroupsResponse", "Data", "DataGroup"]


class DataGroup(BaseModel):
    id: int
    """The unique identifier of the smart group"""

    name: str
    """The name of the smart group"""

    number_of_users: int = FieldInfo(alias="numberOfUsers")
    """The total number of users in the group (excluding admins)"""


class Data(BaseModel):
    groups: List[DataGroup]
    """The smart groups"""


class V1GetSmartGroupsResponse(BaseModel):
    data: Data

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
