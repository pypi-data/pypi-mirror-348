# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel
from .jobs_response import JobsResponse
from ...settings.v1.paging_response import PagingResponse

__all__ = ["JobListResponse"]


class JobListResponse(BaseModel):
    data: JobsResponse

    paging: PagingResponse

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
