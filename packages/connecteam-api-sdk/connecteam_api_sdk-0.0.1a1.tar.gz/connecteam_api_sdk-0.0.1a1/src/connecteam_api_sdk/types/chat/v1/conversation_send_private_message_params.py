# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from ...._utils import PropertyInfo

__all__ = [
    "ConversationSendPrivateMessageParams",
    "Attachment",
    "AttachmentImageAttachmentRequest",
    "AttachmentFileAttachmentRequest",
]


class ConversationSendPrivateMessageParams(TypedDict, total=False):
    sender_id: Required[Annotated[int, PropertyInfo(alias="senderId")]]
    """The unique identifier of the sender (custom publisher).

    The custom publishers page can be found in the UI under Settings -> Feed
    settings.
    """

    text: Required[str]
    """Specifies the text content of the message.

    Must be in UTF-8 and less than 500 characters.
    """

    attachments: Iterable[Attachment]
    """List of attachments to be associated with the message."""


class AttachmentImageAttachmentRequest(TypedDict, total=False):
    file_id: Required[Annotated[str, PropertyInfo(alias="fileId")]]
    """The unique identifier of the image."""

    type: Required[Literal["image"]]
    """The type of the attachment."""


class AttachmentFileAttachmentRequest(TypedDict, total=False):
    file_id: Required[Annotated[str, PropertyInfo(alias="fileId")]]
    """The unique identifier of the file."""

    type: Required[Literal["file"]]
    """The type of the attachment."""


Attachment: TypeAlias = Union[AttachmentImageAttachmentRequest, AttachmentFileAttachmentRequest]
