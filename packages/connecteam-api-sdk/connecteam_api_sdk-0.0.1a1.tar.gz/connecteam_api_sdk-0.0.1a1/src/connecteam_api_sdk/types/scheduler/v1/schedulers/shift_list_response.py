# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ....._models import BaseModel
from .shift_bulk_response import ShiftBulkResponse
from ....settings.v1.paging_response import PagingResponse

__all__ = ["ShiftListResponse"]


class ShiftListResponse(BaseModel):
    data: ShiftBulkResponse

    paging: PagingResponse

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
