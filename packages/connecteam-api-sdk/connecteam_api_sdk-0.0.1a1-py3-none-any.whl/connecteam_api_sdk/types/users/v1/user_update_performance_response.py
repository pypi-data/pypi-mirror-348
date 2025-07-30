# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["UserUpdatePerformanceResponse", "Data"]


class Data(BaseModel):
    records_affected: int = FieldInfo(alias="recordsAffected")
    """Number of records affected by the update operation"""


class UserUpdatePerformanceResponse(BaseModel):
    data: Data
    """Response model for performance data update endpoint."""

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
