# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ......_models import BaseModel

__all__ = ["AutoAssignCreateRequestResponse", "Data"]


class Data(BaseModel):
    auto_assign_request_id: str = FieldInfo(alias="autoAssignRequestId")
    """The unique identifier of the auto assign request"""


class AutoAssignCreateRequestResponse(BaseModel):
    data: Data

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
