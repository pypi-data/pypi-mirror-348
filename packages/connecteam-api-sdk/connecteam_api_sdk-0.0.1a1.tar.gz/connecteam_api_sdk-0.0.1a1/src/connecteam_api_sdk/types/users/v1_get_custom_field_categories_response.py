# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from ..settings.v1.paging_response import PagingResponse

__all__ = ["V1GetCustomFieldCategoriesResponse", "Data", "DataCategory"]


class DataCategory(BaseModel):
    id: int
    """The category's id"""

    name: str
    """The category's name"""


class Data(BaseModel):
    categories: List[DataCategory]
    """The custom fields categories"""


class V1GetCustomFieldCategoriesResponse(BaseModel):
    data: Data

    paging: PagingResponse

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
