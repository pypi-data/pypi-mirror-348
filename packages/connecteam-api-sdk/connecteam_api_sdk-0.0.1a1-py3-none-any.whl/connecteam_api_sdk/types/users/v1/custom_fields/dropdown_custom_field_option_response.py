# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ....._models import BaseModel

__all__ = ["DropdownCustomFieldOptionResponse"]


class DropdownCustomFieldOptionResponse(BaseModel):
    id: int
    """The id of this option"""

    value: str
    """The name of this option"""

    is_deleted: Optional[bool] = FieldInfo(alias="isDeleted", default=None)
    """
    Indicates if this option is deleted (this will still be returned in case someone
    already chose this option so you can see the value).
    """

    is_disabled: Optional[bool] = FieldInfo(alias="isDisabled", default=None)
    """Indicates if this option is disabled"""
