# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ....._models import BaseModel

__all__ = ["ShiftLayerListResponse", "Data", "DataShiftLayer"]


class DataShiftLayer(BaseModel):
    id: str
    """The unique identifier of the shift layer"""

    title: str
    """The name of the shift layer"""


class Data(BaseModel):
    shift_layers: Optional[List[DataShiftLayer]] = FieldInfo(alias="shiftLayers", default=None)
    """The various layers of information associated with shifts in this scheduler"""


class ShiftLayerListResponse(BaseModel):
    data: Data

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
