# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["OptionCreateParams"]


class OptionCreateParams(TypedDict, total=False):
    value: Required[str]
    """The value to be added as the option"""

    is_disabled: Annotated[bool, PropertyInfo(alias="isDisabled")]
    """Indicates if this option is disabled"""
