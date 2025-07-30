# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal, TypeAlias

__all__ = ["UserCustomFields"]

UserCustomFields: TypeAlias = Literal[
    "email", "date", "phone", "number", "str", "dropdown", "file", "directManager", "birthday"
]
