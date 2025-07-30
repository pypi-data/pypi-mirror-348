# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ....._models import BaseModel

__all__ = ["TimeOffUserBalance"]


class TimeOffUserBalance(BaseModel):
    balance: float
    """The remaining user balance"""

    units: Literal["hours", "days"]
    """An enumeration."""

    user_id: int = FieldInfo(alias="userId")
    """The user id"""
