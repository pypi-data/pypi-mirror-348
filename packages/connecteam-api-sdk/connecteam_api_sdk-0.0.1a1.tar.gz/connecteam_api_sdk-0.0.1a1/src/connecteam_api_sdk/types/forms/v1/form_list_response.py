# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel
from .form_response import FormResponse
from ...settings.v1.paging_response import PagingResponse

__all__ = ["FormListResponse", "Data"]


class Data(BaseModel):
    forms: List[FormResponse]
    """List of company's forms"""


class FormListResponse(BaseModel):
    data: Data

    paging: PagingResponse

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
