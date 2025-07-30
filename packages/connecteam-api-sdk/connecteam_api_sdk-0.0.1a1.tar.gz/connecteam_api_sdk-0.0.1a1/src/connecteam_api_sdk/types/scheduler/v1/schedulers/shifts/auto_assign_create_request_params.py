# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, Annotated, TypedDict

from ......_utils import PropertyInfo

__all__ = ["AutoAssignCreateRequestParams"]


class AutoAssignCreateRequestParams(TypedDict, total=False):
    shifts_ids: Required[Annotated[List[str], PropertyInfo(alias="shiftsIds")]]
    """List of shift IDs to start a request to auto assign.

    The shifts must be within the same week period (according to the scheduler
    settings).
    """

    is_force_limitations: Annotated[bool, PropertyInfo(alias="isForceLimitations")]
    """Determines whether to consider users' limitations."""

    is_force_open_shift_requests: Annotated[bool, PropertyInfo(alias="isForceOpenShiftRequests")]
    """Determines whether to assign open shifts exclusively to requesters.

    If set to false, it first prioritizes requesters, then assigns the remaining.
    """

    is_force_qualification: Annotated[bool, PropertyInfo(alias="isForceQualification")]
    """Determines whether to take into consideration the qualifications of users."""

    is_force_unavailability: Annotated[bool, PropertyInfo(alias="isForceUnavailability")]
    """Determines whether to consider users' unavailabilities."""
