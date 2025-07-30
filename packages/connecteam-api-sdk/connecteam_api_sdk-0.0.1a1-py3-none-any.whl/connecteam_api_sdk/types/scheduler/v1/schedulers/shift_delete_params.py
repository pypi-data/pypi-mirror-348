# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["ShiftDeleteParams"]


class ShiftDeleteParams(TypedDict, total=False):
    shifts_ids: Required[Annotated[List[str], PropertyInfo(alias="shiftsIds")]]
    """The unique identifiers of the shifts to delete"""

    notify_users: Annotated[bool, PropertyInfo(alias="notifyUsers")]
    """Indicates whether to send a notification to the users assigned to the shifts.

    This applies only to shifts that are published.
    """
