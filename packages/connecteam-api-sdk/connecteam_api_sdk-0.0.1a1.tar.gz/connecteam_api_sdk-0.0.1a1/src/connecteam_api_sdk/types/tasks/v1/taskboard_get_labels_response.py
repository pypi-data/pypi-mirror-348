# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel
from ...settings.v1.paging_response import PagingResponse

__all__ = ["TaskboardGetLabelsResponse", "Data", "DataLabel"]


class DataLabel(BaseModel):
    id: str
    """The ID of the task label"""

    color: str
    """The color of the task label"""

    name: str
    """The name of the task label"""


class Data(BaseModel):
    labels: List[DataLabel]
    """List of task labels"""


class TaskboardGetLabelsResponse(BaseModel):
    data: Data

    paging: PagingResponse

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
