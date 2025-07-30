# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ....._models import BaseModel
from .time_off_user_balance import TimeOffUserBalance
from ....settings.v1.paging_response import PagingResponse

__all__ = ["BalanceListResponse", "Data"]


class Data(BaseModel):
    balances: List[TimeOffUserBalance]
    """List of user balances of the policy type"""


class BalanceListResponse(BaseModel):
    data: Data

    paging: PagingResponse

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
