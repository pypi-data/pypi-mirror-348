# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["LimitAdminsWhoCanEdit"]


class LimitAdminsWhoCanEdit(BaseModel):
    admins_who_can_edit: List[int] = FieldInfo(alias="adminsWhoCanEdit")
    """List of user IDs of admins that can change this Manager Field"""

    direct_manager_permitted: bool = FieldInfo(alias="directManagerPermitted")
    """
    Indication if the direct manager of the user who submitted the form can edit the
    manager field
    """

    enabled: bool
    """Indication if the limit of which admins can edit the Manager Field is enabled"""

    specific_users_enabled: bool = FieldInfo(alias="specificUsersEnabled")
    """Indication if there are specific admins permitted to edit the manager field"""
