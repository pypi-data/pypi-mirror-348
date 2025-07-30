# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["V1CreateDailyNoteParams"]


class V1CreateDailyNoteParams(TypedDict, total=False):
    date: Required[str]
    """The date for the note in ISO 8601 format (e.g. YYYY-MM-DD)"""

    instance_id: Required[Annotated[int, PropertyInfo(alias="instanceId")]]
    """The unique identifier of the scheduler"""

    title: Required[str]
    """The title of the note"""

    qualified_group_ids: Annotated[Iterable[int], PropertyInfo(alias="qualifiedGroupIds")]
    """The groups qualified to see the note"""

    qualified_user_ids: Annotated[Iterable[int], PropertyInfo(alias="qualifiedUserIds")]
    """The users qualified to see the note"""
