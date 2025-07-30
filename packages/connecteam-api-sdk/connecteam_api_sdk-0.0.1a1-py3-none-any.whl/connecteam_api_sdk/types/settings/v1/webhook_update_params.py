# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["WebhookUpdateParams"]


class WebhookUpdateParams(TypedDict, total=False):
    event_types: Annotated[List[str], PropertyInfo(alias="eventTypes")]
    """The event types under the specified feature type.

    The list of events is available in the Guides section or on the platform.
    """

    feature_type: Annotated[str, PropertyInfo(alias="featureType")]
    """The feature type of the webhook.

    Current options are: users, forms, time_activity, tasks
    """

    is_disabled: Annotated[bool, PropertyInfo(alias="isDisabled")]
    """Determines whether the webhook settings is disabled or enabled upon creation.

    Default to enabled.
    """

    name: str
    """The name of the webhook"""

    object_id: Annotated[int, PropertyInfo(alias="objectId")]
    """The ID of the specified object (e.g.

    for time activities webhook, specify the time clock ID)
    """

    secret_key: Annotated[str, PropertyInfo(alias="secretKey")]
    """The secret key for this webhook"""

    url: str
    """
    The specified endpoint url the payload will be sent to when the event is
    triggered. Must be a valid https endpoint.
    """
