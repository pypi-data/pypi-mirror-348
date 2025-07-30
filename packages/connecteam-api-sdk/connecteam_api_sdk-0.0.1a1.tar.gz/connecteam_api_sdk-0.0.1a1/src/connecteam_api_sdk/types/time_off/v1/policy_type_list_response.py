# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["PolicyTypeListResponse", "Data", "DataPolicyType"]


class DataPolicyType(BaseModel):
    id: str
    """The policy type id"""

    name: str
    """The policy type name"""


class Data(BaseModel):
    policy_types: List[DataPolicyType] = FieldInfo(alias="policyTypes")
    """List of the company policy types"""


class PolicyTypeListResponse(BaseModel):
    data: Data

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
