# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["V1PromoteAdminParams"]


class V1PromoteAdminParams(TypedDict, total=False):
    email: Required[str]
    """The email address of the user to be promoted.

    An invitation link will be sent to the specified email. Once the user
    acknowledges the email, the user will become an admin of the account.
    """

    title: Required[str]
    """The title of the user to be promoted"""

    user_id: Required[Annotated[int, PropertyInfo(alias="userId")]]
    """The unique identifier of the user to be promoted to admin"""
