# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["UserCreateNoteResponse", "Data"]


class Data(BaseModel):
    id: int
    """The unique identifier of the note"""

    created_at: int = FieldInfo(alias="createdAt")
    """The timestamp (in Unix) when the note was created"""

    created_by: int = FieldInfo(alias="createdBy")
    """The user ID who created the note"""

    modified_at: int = FieldInfo(alias="modifiedAt")
    """The timestamp (in Unix) when the note was recently modified"""

    modified_by: int = FieldInfo(alias="modifiedBy")
    """The user ID who modified the note for the last time"""

    text: str
    """Specifies the text content of the message.

    Must be in UTF-8 and less than 1000 characters.
    """

    title: Optional[str] = None
    """The title of the note"""


class UserCreateNoteResponse(BaseModel):
    data: Data

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
