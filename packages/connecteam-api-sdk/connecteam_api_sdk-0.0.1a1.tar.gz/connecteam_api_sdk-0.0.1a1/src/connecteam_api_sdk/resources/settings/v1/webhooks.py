# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.settings.v1 import webhook_list_params, webhook_create_params, webhook_update_params
from ....types.settings.v1.webhook_list_response import WebhookListResponse
from ....types.settings.v1.webhook_delete_response import WebhookDeleteResponse
from ....types.settings.v1.public_base_webhook_response import PublicBaseWebhookResponse

__all__ = ["WebhooksResource", "AsyncWebhooksResource"]


class WebhooksResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> WebhooksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return WebhooksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> WebhooksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return WebhooksResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        event_types: List[str],
        feature_type: str,
        name: str,
        url: str,
        is_disabled: bool | NotGiven = NOT_GIVEN,
        object_id: int | NotGiven = NOT_GIVEN,
        secret_key: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PublicBaseWebhookResponse:
        """
        Create individual webhook settings under specified details

        Args:
          event_types: The event types under the specified feature type. The list of events is
              available in the Guides section or on the platform.

          feature_type: The feature type of the webhook. Current options are: users, forms,
              time_activity, tasks

          name: The name of the webhook

          url: The specified endpoint url the payload will be sent to when the event is
              triggered. Must be a valid https endpoint.

          is_disabled: Determines whether the webhook settings is disabled or enabled upon creation.
              Default to enabled.

          object_id: The ID of the specified object (e.g. for time activities webhook, specify the
              time clock ID)

          secret_key: The secret key for this webhook

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/settings/v1/webhooks",
            body=maybe_transform(
                {
                    "event_types": event_types,
                    "feature_type": feature_type,
                    "name": name,
                    "url": url,
                    "is_disabled": is_disabled,
                    "object_id": object_id,
                    "secret_key": secret_key,
                },
                webhook_create_params.WebhookCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PublicBaseWebhookResponse,
        )

    def retrieve(
        self,
        webhook_id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PublicBaseWebhookResponse:
        """
        Retrieve single webhook information by its unique ID

        Args:
          webhook_id: The unique identifier of the webhook

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            f"/settings/v1/webhooks/{webhook_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PublicBaseWebhookResponse,
        )

    def update(
        self,
        webhook_id: int,
        *,
        event_types: List[str] | NotGiven = NOT_GIVEN,
        feature_type: str | NotGiven = NOT_GIVEN,
        is_disabled: bool | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        object_id: int | NotGiven = NOT_GIVEN,
        secret_key: str | NotGiven = NOT_GIVEN,
        url: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PublicBaseWebhookResponse:
        """
        Update an existing webhook settings by its unique ID.

        Args:
          webhook_id: The unique identifier of the webhook

          event_types: The event types under the specified feature type. The list of events is
              available in the Guides section or on the platform.

          feature_type: The feature type of the webhook. Current options are: users, forms,
              time_activity, tasks

          is_disabled: Determines whether the webhook settings is disabled or enabled upon creation.
              Default to enabled.

          name: The name of the webhook

          object_id: The ID of the specified object (e.g. for time activities webhook, specify the
              time clock ID)

          secret_key: The secret key for this webhook

          url: The specified endpoint url the payload will be sent to when the event is
              triggered. Must be a valid https endpoint.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._put(
            f"/settings/v1/webhooks/{webhook_id}",
            body=maybe_transform(
                {
                    "event_types": event_types,
                    "feature_type": feature_type,
                    "is_disabled": is_disabled,
                    "name": name,
                    "object_id": object_id,
                    "secret_key": secret_key,
                    "url": url,
                },
                webhook_update_params.WebhookUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PublicBaseWebhookResponse,
        )

    def list(
        self,
        *,
        feature_type: str | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WebhookListResponse:
        """
        Retrieves a list of webhook settings associated with the account.

        Args:
          feature_type: The feature type of the webhook. Current options are: users, forms,
              time_activity, tasks

          limit: The maximum number of results to display per page

          offset: The resource offset of the last successfully read resource will be returned as
              the paging.offset JSON property of a paginated response containing more results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/settings/v1/webhooks",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "feature_type": feature_type,
                        "limit": limit,
                        "offset": offset,
                    },
                    webhook_list_params.WebhookListParams,
                ),
            ),
            cast_to=WebhookListResponse,
        )

    def delete(
        self,
        webhook_id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WebhookDeleteResponse:
        """
        Delete a single webhook configuration by its unique ID

        Args:
          webhook_id: The unique identifier of the webhook

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._delete(
            f"/settings/v1/webhooks/{webhook_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WebhookDeleteResponse,
        )


class AsyncWebhooksResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncWebhooksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncWebhooksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncWebhooksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return AsyncWebhooksResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        event_types: List[str],
        feature_type: str,
        name: str,
        url: str,
        is_disabled: bool | NotGiven = NOT_GIVEN,
        object_id: int | NotGiven = NOT_GIVEN,
        secret_key: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PublicBaseWebhookResponse:
        """
        Create individual webhook settings under specified details

        Args:
          event_types: The event types under the specified feature type. The list of events is
              available in the Guides section or on the platform.

          feature_type: The feature type of the webhook. Current options are: users, forms,
              time_activity, tasks

          name: The name of the webhook

          url: The specified endpoint url the payload will be sent to when the event is
              triggered. Must be a valid https endpoint.

          is_disabled: Determines whether the webhook settings is disabled or enabled upon creation.
              Default to enabled.

          object_id: The ID of the specified object (e.g. for time activities webhook, specify the
              time clock ID)

          secret_key: The secret key for this webhook

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/settings/v1/webhooks",
            body=await async_maybe_transform(
                {
                    "event_types": event_types,
                    "feature_type": feature_type,
                    "name": name,
                    "url": url,
                    "is_disabled": is_disabled,
                    "object_id": object_id,
                    "secret_key": secret_key,
                },
                webhook_create_params.WebhookCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PublicBaseWebhookResponse,
        )

    async def retrieve(
        self,
        webhook_id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PublicBaseWebhookResponse:
        """
        Retrieve single webhook information by its unique ID

        Args:
          webhook_id: The unique identifier of the webhook

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            f"/settings/v1/webhooks/{webhook_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PublicBaseWebhookResponse,
        )

    async def update(
        self,
        webhook_id: int,
        *,
        event_types: List[str] | NotGiven = NOT_GIVEN,
        feature_type: str | NotGiven = NOT_GIVEN,
        is_disabled: bool | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        object_id: int | NotGiven = NOT_GIVEN,
        secret_key: str | NotGiven = NOT_GIVEN,
        url: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PublicBaseWebhookResponse:
        """
        Update an existing webhook settings by its unique ID.

        Args:
          webhook_id: The unique identifier of the webhook

          event_types: The event types under the specified feature type. The list of events is
              available in the Guides section or on the platform.

          feature_type: The feature type of the webhook. Current options are: users, forms,
              time_activity, tasks

          is_disabled: Determines whether the webhook settings is disabled or enabled upon creation.
              Default to enabled.

          name: The name of the webhook

          object_id: The ID of the specified object (e.g. for time activities webhook, specify the
              time clock ID)

          secret_key: The secret key for this webhook

          url: The specified endpoint url the payload will be sent to when the event is
              triggered. Must be a valid https endpoint.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._put(
            f"/settings/v1/webhooks/{webhook_id}",
            body=await async_maybe_transform(
                {
                    "event_types": event_types,
                    "feature_type": feature_type,
                    "is_disabled": is_disabled,
                    "name": name,
                    "object_id": object_id,
                    "secret_key": secret_key,
                    "url": url,
                },
                webhook_update_params.WebhookUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PublicBaseWebhookResponse,
        )

    async def list(
        self,
        *,
        feature_type: str | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WebhookListResponse:
        """
        Retrieves a list of webhook settings associated with the account.

        Args:
          feature_type: The feature type of the webhook. Current options are: users, forms,
              time_activity, tasks

          limit: The maximum number of results to display per page

          offset: The resource offset of the last successfully read resource will be returned as
              the paging.offset JSON property of a paginated response containing more results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/settings/v1/webhooks",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "feature_type": feature_type,
                        "limit": limit,
                        "offset": offset,
                    },
                    webhook_list_params.WebhookListParams,
                ),
            ),
            cast_to=WebhookListResponse,
        )

    async def delete(
        self,
        webhook_id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WebhookDeleteResponse:
        """
        Delete a single webhook configuration by its unique ID

        Args:
          webhook_id: The unique identifier of the webhook

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._delete(
            f"/settings/v1/webhooks/{webhook_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WebhookDeleteResponse,
        )


class WebhooksResourceWithRawResponse:
    def __init__(self, webhooks: WebhooksResource) -> None:
        self._webhooks = webhooks

        self.create = to_raw_response_wrapper(
            webhooks.create,
        )
        self.retrieve = to_raw_response_wrapper(
            webhooks.retrieve,
        )
        self.update = to_raw_response_wrapper(
            webhooks.update,
        )
        self.list = to_raw_response_wrapper(
            webhooks.list,
        )
        self.delete = to_raw_response_wrapper(
            webhooks.delete,
        )


class AsyncWebhooksResourceWithRawResponse:
    def __init__(self, webhooks: AsyncWebhooksResource) -> None:
        self._webhooks = webhooks

        self.create = async_to_raw_response_wrapper(
            webhooks.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            webhooks.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            webhooks.update,
        )
        self.list = async_to_raw_response_wrapper(
            webhooks.list,
        )
        self.delete = async_to_raw_response_wrapper(
            webhooks.delete,
        )


class WebhooksResourceWithStreamingResponse:
    def __init__(self, webhooks: WebhooksResource) -> None:
        self._webhooks = webhooks

        self.create = to_streamed_response_wrapper(
            webhooks.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            webhooks.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            webhooks.update,
        )
        self.list = to_streamed_response_wrapper(
            webhooks.list,
        )
        self.delete = to_streamed_response_wrapper(
            webhooks.delete,
        )


class AsyncWebhooksResourceWithStreamingResponse:
    def __init__(self, webhooks: AsyncWebhooksResource) -> None:
        self._webhooks = webhooks

        self.create = async_to_streamed_response_wrapper(
            webhooks.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            webhooks.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            webhooks.update,
        )
        self.list = async_to_streamed_response_wrapper(
            webhooks.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            webhooks.delete,
        )
