# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from pydantic import Field as FieldInfo

from ....._models import BaseModel

__all__ = ["ManagerFieldFile"]


class ManagerFieldFile(BaseModel):
    filename: str
    """The name of the file."""

    file_url: str = FieldInfo(alias="fileUrl")
    """The URL of the file."""
