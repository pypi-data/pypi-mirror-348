# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["ManagerFieldStatusOptionParam"]


class ManagerFieldStatusOptionParam(TypedDict, total=False):
    color: Required[str]
    """The color of the status option."""

    name: Required[str]
    """The name of the status option."""

    status_option_id: Required[Annotated[str, PropertyInfo(alias="statusOptionId")]]
    """The ID of the status option."""
