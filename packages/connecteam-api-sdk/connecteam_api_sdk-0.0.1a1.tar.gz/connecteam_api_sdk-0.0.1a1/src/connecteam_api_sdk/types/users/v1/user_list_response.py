# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .user import User
from ...._models import BaseModel
from ...settings.v1.paging_response import PagingResponse

__all__ = ["UserListResponse", "Data"]


class Data(BaseModel):
    users: List[User]
    """The users."""


class UserListResponse(BaseModel):
    data: Data

    paging: PagingResponse

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
