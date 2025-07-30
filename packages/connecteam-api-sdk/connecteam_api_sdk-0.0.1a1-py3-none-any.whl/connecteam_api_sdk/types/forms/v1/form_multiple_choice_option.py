# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["FormMultipleChoiceOption"]


class FormMultipleChoiceOption(BaseModel):
    multiple_choice_option_id: str = FieldInfo(alias="multipleChoiceOptionId")
    """The ID of the multiple choice option"""

    text: str
    """The text of the option"""
