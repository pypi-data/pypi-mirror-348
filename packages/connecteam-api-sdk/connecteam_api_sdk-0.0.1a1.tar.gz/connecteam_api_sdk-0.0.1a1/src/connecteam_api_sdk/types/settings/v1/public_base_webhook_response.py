# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["PublicBaseWebhookResponse", "Data"]


class Data(BaseModel):
    id: int
    """The unique identifier of the webhook"""

    event_types: List[str] = FieldInfo(alias="eventTypes")
    """The webhook's event types"""

    feature_type: str = FieldInfo(alias="featureType")
    """The webhook's feature type"""

    is_disabled: bool = FieldInfo(alias="isDisabled")
    """The webhook's disabled status"""

    name: str
    """The name of the webhook"""

    retry_limit: int = FieldInfo(alias="retryLimit")
    """The webhook's retry limit"""

    time_created: int = FieldInfo(alias="timeCreated")
    """The timestamp when the webhook was created"""

    url: str
    """The webhook's URL"""

    user_id: int = FieldInfo(alias="userId")
    """Webhook creator's user id"""

    object_id: Optional[int] = FieldInfo(alias="objectId", default=None)
    """The webhook's object id"""


class PublicBaseWebhookResponse(BaseModel):
    data: Data

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
