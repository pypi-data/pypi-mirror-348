# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from pydantic import Field as FieldInfo

from ....._models import BaseModel

__all__ = ["ManagerFieldStatusOption"]


class ManagerFieldStatusOption(BaseModel):
    color: str
    """The color of the status option."""

    name: str
    """The name of the status option."""

    status_option_id: str = FieldInfo(alias="statusOptionId")
    """The ID of the status option."""
