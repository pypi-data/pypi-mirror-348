# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from ..settings.v1.paging_response import PagingResponse

__all__ = ["V1ListResponse", "Data", "DataPublisher"]


class DataPublisher(BaseModel):
    id: int
    """The unique identifier of the publisher"""

    image_url: str = FieldInfo(alias="imageUrl")
    """The image url of the publisher"""

    name: str
    """The name of the publisher"""


class Data(BaseModel):
    publishers: List[DataPublisher]
    """The list of publishers"""


class V1ListResponse(BaseModel):
    data: Data

    paging: PagingResponse

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
