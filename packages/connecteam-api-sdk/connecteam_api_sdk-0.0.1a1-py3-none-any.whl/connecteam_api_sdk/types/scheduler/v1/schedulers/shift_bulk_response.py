# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ....._models import BaseModel
from .shift_response_scheduler import ShiftResponseScheduler

__all__ = ["ShiftBulkResponse"]


class ShiftBulkResponse(BaseModel):
    shifts: List[ShiftResponseScheduler]
    """The shifts"""
