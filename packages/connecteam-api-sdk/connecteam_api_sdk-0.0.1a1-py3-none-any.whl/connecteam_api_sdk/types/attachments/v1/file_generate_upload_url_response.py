# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["FileGenerateUploadURLResponse", "Data"]


class Data(BaseModel):
    file_id: str = FieldInfo(alias="fileId")
    """The unique identifier for the file"""

    upload_file_url: str = FieldInfo(alias="uploadFileUrl")
    """The pre-signed URL for uploading the file to the cloud storage"""


class FileGenerateUploadURLResponse(BaseModel):
    data: Data

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
