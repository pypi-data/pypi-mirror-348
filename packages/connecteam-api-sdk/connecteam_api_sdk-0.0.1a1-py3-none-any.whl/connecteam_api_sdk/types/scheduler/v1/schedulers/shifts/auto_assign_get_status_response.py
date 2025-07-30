# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ......_models import BaseModel

__all__ = ["AutoAssignGetStatusResponse", "Data"]


class Data(BaseModel):
    auto_assign_request_id: str = FieldInfo(alias="autoAssignRequestId")
    """The unique identifier of the auto assign request"""

    assigned_shift_ids: Optional[List[str]] = FieldInfo(alias="assignedShiftIds", default=None)
    """List of shift IDs that were successfully assigned"""

    status: Optional[str] = None
    """The status of the request"""

    unassigned_shift_ids: Optional[List[str]] = FieldInfo(alias="unassignedShiftIds", default=None)
    """List of shift IDs that were not successfully assigned"""


class AutoAssignGetStatusResponse(BaseModel):
    data: Data

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
