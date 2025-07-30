# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ....._models import BaseModel
from .form_submission import FormSubmission

__all__ = ["FormSubmissionRetrieveResponse", "Data"]


class Data(BaseModel):
    form_submission: FormSubmission = FieldInfo(alias="formSubmission")
    """The form submission."""


class FormSubmissionRetrieveResponse(BaseModel):
    data: Data

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
