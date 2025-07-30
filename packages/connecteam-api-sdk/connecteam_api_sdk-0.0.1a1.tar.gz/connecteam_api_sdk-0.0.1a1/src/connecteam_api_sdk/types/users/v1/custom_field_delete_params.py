# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["CustomFieldDeleteParams"]


class CustomFieldDeleteParams(TypedDict, total=False):
    custom_field_ids: Required[Annotated[Iterable[int], PropertyInfo(alias="customFieldIds")]]
    """The custom fields IDs to delete"""
