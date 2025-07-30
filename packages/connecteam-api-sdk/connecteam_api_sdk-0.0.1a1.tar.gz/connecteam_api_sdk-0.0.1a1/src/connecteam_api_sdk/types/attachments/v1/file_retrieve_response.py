# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["FileRetrieveResponse", "Data"]


class Data(BaseModel):
    feature_type: str = FieldInfo(alias="featureType")
    """Feature type"""

    file_id: str = FieldInfo(alias="fileId")
    """The unique identifier for the file"""

    file_type: str = FieldInfo(alias="fileType")
    """The MIME type or format of the file"""

    upload_completed: bool = FieldInfo(alias="uploadCompleted")
    """
    Indicates whether the upload process for the file has been successfully
    completed
    """

    file_url: Optional[str] = FieldInfo(alias="fileUrl", default=None)
    """The file URL"""


class FileRetrieveResponse(BaseModel):
    data: Data

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
