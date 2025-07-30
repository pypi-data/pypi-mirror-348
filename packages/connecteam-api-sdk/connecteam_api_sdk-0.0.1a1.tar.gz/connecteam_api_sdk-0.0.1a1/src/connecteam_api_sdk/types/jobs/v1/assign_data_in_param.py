# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Annotated, TypedDict

from ...._utils import PropertyInfo
from .assign_data_types import AssignDataTypes

__all__ = ["AssignDataInParam"]


class AssignDataInParam(TypedDict, total=False):
    group_ids: Annotated[Iterable[int], PropertyInfo(alias="groupIds")]
    """The group ids to assign to this entity (if assigning type is groups)."""

    type: AssignDataTypes
    """An enumeration."""

    user_ids: Annotated[Iterable[int], PropertyInfo(alias="userIds")]
    """The user ids to assign to this entity (if assigning type is users)."""
