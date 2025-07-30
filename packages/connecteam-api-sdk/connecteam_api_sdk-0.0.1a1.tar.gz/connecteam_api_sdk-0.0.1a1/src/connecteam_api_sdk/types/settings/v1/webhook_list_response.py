# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ...._models import BaseModel
from .paging_response import PagingResponse

__all__ = ["WebhookListResponse", "Data", "DataWebhook"]


class DataWebhook(BaseModel):
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

    origin: Optional[Literal["organic", "integration"]] = None
    """An enumeration."""


class Data(BaseModel):
    webhooks: List[DataWebhook]
    """List of webhooks"""


class WebhookListResponse(BaseModel):
    data: Data

    paging: PagingResponse

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
