# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ....._models import BaseModel

__all__ = ["TaskDeleteResponse"]


class TaskDeleteResponse(BaseModel):
    data: object

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
