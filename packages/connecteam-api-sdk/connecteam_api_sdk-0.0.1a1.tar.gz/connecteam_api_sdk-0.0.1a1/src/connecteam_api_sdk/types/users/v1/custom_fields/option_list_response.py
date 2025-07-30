# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ....._models import BaseModel
from ....settings.v1.paging_response import PagingResponse
from .dropdown_custom_field_option_response import DropdownCustomFieldOptionResponse

__all__ = ["OptionListResponse", "Data"]


class Data(BaseModel):
    options: List[DropdownCustomFieldOptionResponse]
    """The custom field options"""


class OptionListResponse(BaseModel):
    data: Data

    paging: PagingResponse

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
