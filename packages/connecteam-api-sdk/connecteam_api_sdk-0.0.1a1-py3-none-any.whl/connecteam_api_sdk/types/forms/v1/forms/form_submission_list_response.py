# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ....._models import BaseModel
from .form_submission import FormSubmission
from ....settings.v1.paging_response import PagingResponse

__all__ = ["FormSubmissionListResponse", "Data"]


class Data(BaseModel):
    form_submissions: List[FormSubmission] = FieldInfo(alias="formSubmissions")
    """A list of form submissions."""


class FormSubmissionListResponse(BaseModel):
    data: Data

    paging: PagingResponse

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
