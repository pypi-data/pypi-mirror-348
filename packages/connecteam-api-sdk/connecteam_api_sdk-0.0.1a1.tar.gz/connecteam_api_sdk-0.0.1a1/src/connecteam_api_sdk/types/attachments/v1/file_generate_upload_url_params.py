# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["FileGenerateUploadURLParams"]


class FileGenerateUploadURLParams(TypedDict, total=False):
    feature_type: Required[Annotated[Literal["chat", "shiftscheduler", "users"], PropertyInfo(alias="featureType")]]
    """An enumeration."""

    file_name: Required[Annotated[str, PropertyInfo(alias="fileName")]]
    """The name of the attachment you want to upload"""

    file_type_hint: Annotated[str, PropertyInfo(alias="fileTypeHint")]
    """The MIME type or format of the attachment (e.g. image/jpeg, application/pdf)"""
