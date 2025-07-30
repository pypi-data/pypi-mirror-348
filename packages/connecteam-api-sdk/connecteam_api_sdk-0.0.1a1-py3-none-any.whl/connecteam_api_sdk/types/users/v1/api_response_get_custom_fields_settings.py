# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel
from .get_custom_fields_settings import GetCustomFieldsSettings

__all__ = ["APIResponseGetCustomFieldsSettings"]


class APIResponseGetCustomFieldsSettings(BaseModel):
    data: GetCustomFieldsSettings

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
