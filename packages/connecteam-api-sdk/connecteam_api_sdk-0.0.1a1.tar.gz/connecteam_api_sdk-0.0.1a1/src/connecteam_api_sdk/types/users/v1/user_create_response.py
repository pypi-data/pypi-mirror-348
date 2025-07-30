# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .user import User
from ...._models import BaseModel

__all__ = ["UserCreateResponse", "Data"]


class Data(BaseModel):
    results: List[User]
    """The created users."""


class UserCreateResponse(BaseModel):
    data: Data

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
