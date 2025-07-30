# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["DailyNoteUpdateParams"]


class DailyNoteUpdateParams(TypedDict, total=False):
    qualified_group_ids: Annotated[Iterable[int], PropertyInfo(alias="qualifiedGroupIds")]
    """The groups qualified to see the note"""

    qualified_user_ids: Annotated[Iterable[int], PropertyInfo(alias="qualifiedUserIds")]
    """The users qualified to see the note"""

    title: str
    """The title of the note"""
