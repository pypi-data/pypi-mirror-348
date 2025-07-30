# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["UserArchiveResponse", "Data"]


class Data(BaseModel):
    success: bool
    """Whether the users were deleted successfully."""


class UserArchiveResponse(BaseModel):
    data: Data

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
