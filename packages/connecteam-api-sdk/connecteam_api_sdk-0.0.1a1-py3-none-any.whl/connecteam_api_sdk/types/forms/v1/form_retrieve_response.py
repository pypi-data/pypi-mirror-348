# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel
from .form_response import FormResponse

__all__ = ["FormRetrieveResponse"]


class FormRetrieveResponse(BaseModel):
    data: FormResponse

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
