# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .user import User
from ...._models import BaseModel

__all__ = ["UserUpdateResponse", "Data"]


class Data(BaseModel):
    count: int
    """The number of users edited."""

    users: List[User]
    """The edited users."""


class UserUpdateResponse(BaseModel):
    data: Data

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
