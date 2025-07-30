# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ....._models import BaseModel
from .form_submission import FormSubmission

__all__ = ["FormSubmissionUpdateResponse", "Data"]


class Data(BaseModel):
    form_submission: List[FormSubmission] = FieldInfo(alias="formSubmission")
    """A list of form submissions."""


class FormSubmissionUpdateResponse(BaseModel):
    data: Data

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
