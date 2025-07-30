# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["CustomFieldDeleteResponse", "Data"]


class Data(BaseModel):
    custom_field_ids: List[int] = FieldInfo(alias="customFieldIds")
    """The deleted custom fields ids"""

    success: bool
    """Whether the custom field were deleted successfully."""


class CustomFieldDeleteResponse(BaseModel):
    data: Data

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
