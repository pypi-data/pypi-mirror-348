# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["BaseCustomFieldParam"]


class BaseCustomFieldParam(TypedDict, total=False):
    custom_field_id: Required[Annotated[int, PropertyInfo(alias="customFieldId")]]
    """The custom field unique id"""

    value: Required[object]
    """The value of the custom field.

    Our real-time API documentation experience does not support custom fields of the
    dropdown type.To update dropdown fields value(s), pass an array of objects with
    the IDs of the selected dropdown values (e.g., [{id: 1}, {id: 2}]).
    """
