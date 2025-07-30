# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel
from .jobs_response import JobsResponse

__all__ = ["JobCreateResponse"]


class JobCreateResponse(BaseModel):
    data: JobsResponse

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
