# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ...._models import BaseModel

__all__ = ["PagingResponse"]


class PagingResponse(BaseModel):
    offset: int
    """
    The resource offset of the last successfully read resource will be returned as
    the paging.offset JSON property of a paginated response containing more results
    """
