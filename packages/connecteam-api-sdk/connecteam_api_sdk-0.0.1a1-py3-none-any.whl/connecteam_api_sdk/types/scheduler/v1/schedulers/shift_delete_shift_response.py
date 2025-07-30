# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ....._models import BaseModel

__all__ = ["ShiftDeleteShiftResponse", "Data"]


class Data(BaseModel):
    shift_id: str = FieldInfo(alias="shiftId")
    """The ID of the deleted shift"""


class ShiftDeleteShiftResponse(BaseModel):
    data: Data

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
