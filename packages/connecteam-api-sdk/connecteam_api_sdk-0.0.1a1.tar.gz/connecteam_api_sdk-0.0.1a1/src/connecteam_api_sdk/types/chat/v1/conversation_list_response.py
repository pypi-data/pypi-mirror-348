# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ...._models import BaseModel
from ...settings.v1.paging_response import PagingResponse

__all__ = ["ConversationListResponse", "Data", "DataConversation"]


class DataConversation(BaseModel):
    id: str
    """The unique identifier of the conversation"""

    title: str
    """The title of the conversation"""

    type: Literal["team", "channel"]
    """An enumeration."""


class Data(BaseModel):
    conversations: List[DataConversation]
    """The list of conversations"""


class ConversationListResponse(BaseModel):
    data: Data

    paging: PagingResponse

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
