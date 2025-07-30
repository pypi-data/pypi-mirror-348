# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal, Annotated, TypedDict

from ...._utils import PropertyInfo
from ...scheduler.v1.schedulers.sort_order import SortOrder

__all__ = ["UserListParams"]


class UserListParams(TypedDict, total=False):
    created_at: Annotated[int, PropertyInfo(alias="createdAt")]
    """Parameter specifying the date in Unix format (in seconds).

    Only users created after this date will be included in the results.
    """

    email_addresses: Annotated[List[str], PropertyInfo(alias="emailAddresses")]
    """List of email addresses to filter by (in format test@test.com)."""

    full_names: Annotated[List[str], PropertyInfo(alias="fullNames")]
    """List of full names to filter by.

    Specify the exact first and last name with a space between them as shown in the
    platform (ignore capitalization).
    """

    limit: int
    """The maximum number of results to display per page"""

    modified_at: Annotated[int, PropertyInfo(alias="modifiedAt")]
    """Parameter specifying the date in in Unix format (in seconds).

    Only users with fields updated after this date will be included in the results.
    """

    offset: int
    """
    The resource offset of the last successfully read resource will be returned as
    the paging.offset JSON property of a paginated response containing more results
    """

    order: SortOrder
    """An enumeration."""

    phone_numbers: Annotated[List[str], PropertyInfo(alias="phoneNumbers")]
    """List of phone numbers to filter by (in format +<country code><phone number>)."""

    sort: Literal["created_at"]
    """An enumeration."""

    user_ids: Annotated[Iterable[int], PropertyInfo(alias="userIds")]
    """List of user IDs for filtering."""

    user_status: Annotated[Literal["active", "archived", "all"], PropertyInfo(alias="userStatus")]
    """An enumeration."""
