# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["ShiftDeleteShiftParams"]


class ShiftDeleteShiftParams(TypedDict, total=False):
    scheduler_id: Required[Annotated[int, PropertyInfo(alias="schedulerId")]]
    """The unique identifier of the scheduler"""

    notify_users: Annotated[bool, PropertyInfo(alias="notifyUsers")]
    """Indicates whether to send a notification to the users assigned to the shifts.

    This applies only to shifts that are published.
    """
