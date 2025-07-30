# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["UserCreateNoteParams"]


class UserCreateNoteParams(TypedDict, total=False):
    text: Required[str]
    """The text of the user note to be created"""

    title: str
    """The title of the user note to be created"""
