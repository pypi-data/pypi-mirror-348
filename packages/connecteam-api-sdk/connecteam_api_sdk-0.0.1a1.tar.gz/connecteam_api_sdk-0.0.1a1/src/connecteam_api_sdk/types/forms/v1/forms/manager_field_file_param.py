# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["ManagerFieldFileParam"]


class ManagerFieldFileParam(TypedDict, total=False):
    filename: Required[str]
    """The name of the file."""

    file_url: Required[Annotated[str, PropertyInfo(alias="fileUrl")]]
    """The URL of the file."""
