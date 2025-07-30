# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ....._models import BaseModel
from .shift_bulk_response import ShiftBulkResponse

__all__ = ["APIResponseShiftBulk"]


class APIResponseShiftBulk(BaseModel):
    data: ShiftBulkResponse

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
