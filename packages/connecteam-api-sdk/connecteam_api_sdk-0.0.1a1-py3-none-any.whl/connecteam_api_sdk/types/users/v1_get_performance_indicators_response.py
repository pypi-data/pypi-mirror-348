# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from ..settings.v1.paging_response import PagingResponse

__all__ = ["V1GetPerformanceIndicatorsResponse", "Data", "DataIndicator"]


class DataIndicator(BaseModel):
    id: int
    """The unique identifier of the indicator"""

    name: str
    """The name of the indicator"""


class Data(BaseModel):
    indicators: List[DataIndicator]
    """List of performance indicators"""


class V1GetPerformanceIndicatorsResponse(BaseModel):
    data: Data
    """Base response model for getting indicators."""

    paging: PagingResponse

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
