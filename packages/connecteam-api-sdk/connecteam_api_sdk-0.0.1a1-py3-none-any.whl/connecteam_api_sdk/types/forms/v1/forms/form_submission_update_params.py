# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from ....._utils import PropertyInfo
from .manager_field_file_param import ManagerFieldFileParam
from .manager_field_status_option_param import ManagerFieldStatusOptionParam

__all__ = [
    "FormSubmissionUpdateParams",
    "ManagerField",
    "ManagerFieldManagerFieldFileRequest",
    "ManagerFieldManagerFieldDateRequest",
    "ManagerFieldManagerFieldSignatureRequest",
    "ManagerFieldManagerFieldOwnerRequest",
    "ManagerFieldManagerFieldStatusRequest",
    "ManagerFieldManagerFieldNoteRequest",
]


class FormSubmissionUpdateParams(TypedDict, total=False):
    form_id: Required[Annotated[int, PropertyInfo(alias="formId")]]
    """Form Id"""

    manager_fields: Required[Annotated[Iterable[ManagerField], PropertyInfo(alias="managerFields")]]
    """The manager fields to update"""


class ManagerFieldManagerFieldFileRequest(TypedDict, total=False):
    files: Required[Iterable[ManagerFieldFileParam]]
    """The files"""

    manager_field_id: Required[Annotated[str, PropertyInfo(alias="managerFieldId")]]
    """The manager field id"""

    manager_field_type: Annotated[Literal["file"], PropertyInfo(alias="managerFieldType")]
    """The manager field type"""


class ManagerFieldManagerFieldDateRequest(TypedDict, total=False):
    date: Required[str]
    """The date"""

    manager_field_id: Required[Annotated[str, PropertyInfo(alias="managerFieldId")]]
    """The manager field id"""

    manager_field_type: Annotated[Literal["date"], PropertyInfo(alias="managerFieldType")]
    """The manager field type"""


class ManagerFieldManagerFieldSignatureRequest(TypedDict, total=False):
    image: Required[str]
    """The signature"""

    manager_field_id: Required[Annotated[str, PropertyInfo(alias="managerFieldId")]]
    """The manager field id"""

    signing_timestamp: Required[Annotated[int, PropertyInfo(alias="signingTimestamp")]]
    """The signing timestamp"""

    signing_user_id: Required[Annotated[int, PropertyInfo(alias="signingUserId")]]
    """The signing user id"""

    manager_field_type: Annotated[Literal["signature"], PropertyInfo(alias="managerFieldType")]
    """The manager field type"""


class ManagerFieldManagerFieldOwnerRequest(TypedDict, total=False):
    manager_field_id: Required[Annotated[str, PropertyInfo(alias="managerFieldId")]]
    """The manager field id"""

    user_id: Required[Annotated[int, PropertyInfo(alias="userId")]]
    """The user id that is the value of the manager field"""

    manager_field_type: Annotated[Literal["owner"], PropertyInfo(alias="managerFieldType")]
    """The manager field type"""


class ManagerFieldManagerFieldStatusRequest(TypedDict, total=False):
    manager_field_id: Required[Annotated[str, PropertyInfo(alias="managerFieldId")]]
    """The manager field id"""

    status: Required[ManagerFieldStatusOptionParam]
    """The status"""

    manager_field_type: Annotated[Literal["status"], PropertyInfo(alias="managerFieldType")]
    """The manager field type"""


class ManagerFieldManagerFieldNoteRequest(TypedDict, total=False):
    manager_field_id: Required[Annotated[str, PropertyInfo(alias="managerFieldId")]]
    """The manager field id"""

    note: Required[str]
    """The note"""

    manager_field_type: Annotated[Literal["note"], PropertyInfo(alias="managerFieldType")]
    """The manager field type"""


ManagerField: TypeAlias = Union[
    ManagerFieldManagerFieldFileRequest,
    ManagerFieldManagerFieldDateRequest,
    ManagerFieldManagerFieldSignatureRequest,
    ManagerFieldManagerFieldOwnerRequest,
    ManagerFieldManagerFieldStatusRequest,
    ManagerFieldManagerFieldNoteRequest,
]
