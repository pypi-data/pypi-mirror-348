# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["MeRetrieveResponse", "Data"]


class Data(BaseModel):
    company_id: str = FieldInfo(alias="companyId")
    """The unique identifier of the company"""

    company_name: str = FieldInfo(alias="companyName")
    """The name of the company"""


class MeRetrieveResponse(BaseModel):
    data: Data

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
