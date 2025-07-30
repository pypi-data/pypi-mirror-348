# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ...._models import BaseModel
from .base_job_response import BaseJobResponse

__all__ = ["JobsResponse"]


class JobsResponse(BaseModel):
    jobs: List[BaseJobResponse]
    """The jobs"""
