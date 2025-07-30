# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["UserUploadPayslipParams"]


class UserUploadPayslipParams(TypedDict, total=False):
    end_date: Required[Annotated[str, PropertyInfo(alias="endDate")]]
    """The end date for the payslip in ISO 8601 format (YYYY-MM-DD)"""

    file_id: Required[Annotated[str, PropertyInfo(alias="fileId")]]
    """The unique identifier of the payslip attachment"""

    start_date: Required[Annotated[str, PropertyInfo(alias="startDate")]]
    """The start date for the payslip in ISO 8601 format (YYYY-MM-DD)"""
