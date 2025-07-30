# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ....._models import BaseModel

__all__ = ["TaskDescription"]


class TaskDescription(BaseModel):
    content: str
    """The content of the description. Must be in UTF-8 format."""
