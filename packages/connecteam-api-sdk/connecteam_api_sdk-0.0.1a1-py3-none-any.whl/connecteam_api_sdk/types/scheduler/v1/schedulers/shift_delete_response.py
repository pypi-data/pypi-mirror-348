# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ....._models import BaseModel

__all__ = ["ShiftDeleteResponse", "Data"]


class Data(BaseModel):
    shifts_ids: List[str] = FieldInfo(alias="shiftsIds")
    """The IDs of the deleted shifts"""


class ShiftDeleteResponse(BaseModel):
    data: Data

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
