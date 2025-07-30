# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import TypeAlias

from pydantic import Field as FieldInfo

from ...._models import BaseModel
from .shift_attachment_type import ShiftAttachmentType

__all__ = [
    "TimeClockGetShiftAttachmentsResponse",
    "Data",
    "DataShiftAttachment",
    "DataShiftAttachmentShiftAttachmentDropDownListSettingsResponse",
    "DataShiftAttachmentShiftAttachmentDropDownListSettingsResponseItem",
    "DataShiftAttachmentShiftAttachmentSettingsResponse",
]


class DataShiftAttachmentShiftAttachmentDropDownListSettingsResponseItem(BaseModel):
    id: str
    """The ID of the dropdown list item"""

    is_enabled: bool = FieldInfo(alias="isEnabled")
    """Whether the dropdown list item is enabled"""

    name: str
    """The name of the dropdown list item"""


class DataShiftAttachmentShiftAttachmentDropDownListSettingsResponse(BaseModel):
    id: str
    """The ID of the shift attachment"""

    is_enabled: bool = FieldInfo(alias="isEnabled")
    """Whether the shift attachment is enabled"""

    is_required: bool = FieldInfo(alias="isRequired")
    """Whether the shift attachment is required"""

    items: List[DataShiftAttachmentShiftAttachmentDropDownListSettingsResponseItem]
    """The dropdown list items"""

    name: str
    """The name of the shift attachment"""

    type: ShiftAttachmentType
    """An enumeration."""


class DataShiftAttachmentShiftAttachmentSettingsResponse(BaseModel):
    id: str
    """The ID of the shift attachment"""

    is_enabled: bool = FieldInfo(alias="isEnabled")
    """Whether the shift attachment is enabled"""

    is_required: bool = FieldInfo(alias="isRequired")
    """Whether the shift attachment is required"""

    name: str
    """The name of the shift attachment"""

    type: ShiftAttachmentType
    """An enumeration."""


DataShiftAttachment: TypeAlias = Union[
    DataShiftAttachmentShiftAttachmentDropDownListSettingsResponse, DataShiftAttachmentShiftAttachmentSettingsResponse
]


class Data(BaseModel):
    shift_attachments: List[DataShiftAttachment] = FieldInfo(alias="shiftAttachments")
    """The shift attachments"""


class TimeClockGetShiftAttachmentsResponse(BaseModel):
    data: Data

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
