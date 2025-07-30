# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel
from .base_job_response import BaseJobResponse

__all__ = ["APIResponse", "Data"]


class Data(BaseModel):
    job: BaseJobResponse
    """The job"""


class APIResponse(BaseModel):
    data: Data

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
