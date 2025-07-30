# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ....._models import BaseModel
from ....settings.v1.paging_response import PagingResponse

__all__ = ["ShiftLayerGetValuesResponse", "Data", "DataValue"]


class DataValue(BaseModel):
    id: str
    """The unique identifier of the shift layer instance"""

    display_name: str = FieldInfo(alias="displayName")
    """The display name of the shift layer instance"""


class Data(BaseModel):
    values: List[DataValue]
    """The values associated to the shift layer"""


class ShiftLayerGetValuesResponse(BaseModel):
    data: Data

    paging: PagingResponse

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
