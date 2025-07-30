# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ....._models import BaseModel
from .time_off_user_balance import TimeOffUserBalance

__all__ = ["BalanceUpdateResponse", "Data"]


class Data(BaseModel):
    balance: TimeOffUserBalance
    """The updated user balance"""


class BalanceUpdateResponse(BaseModel):
    data: Data

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
