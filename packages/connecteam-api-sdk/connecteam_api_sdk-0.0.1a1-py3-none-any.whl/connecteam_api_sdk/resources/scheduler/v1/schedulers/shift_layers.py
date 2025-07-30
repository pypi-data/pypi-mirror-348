# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ....._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ....._utils import maybe_transform, async_maybe_transform
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....._base_client import make_request_options
from .....types.scheduler.v1.schedulers import shift_layer_get_values_params
from .....types.scheduler.v1.schedulers.shift_layer_list_response import ShiftLayerListResponse
from .....types.scheduler.v1.schedulers.shift_layer_get_values_response import ShiftLayerGetValuesResponse

__all__ = ["ShiftLayersResource", "AsyncShiftLayersResource"]


class ShiftLayersResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ShiftLayersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return ShiftLayersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ShiftLayersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return ShiftLayersResourceWithStreamingResponse(self)

    def list(
        self,
        scheduler_id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ShiftLayerListResponse:
        """
        Retrieve a list of shift layers under a specified scheduler

        Args:
          scheduler_id: The unique identifier of the scheduler

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            f"/scheduler/v1/schedulers/{scheduler_id}/shift-layers",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ShiftLayerListResponse,
        )

    def get_values(
        self,
        layer_id: str,
        *,
        scheduler_id: int,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ShiftLayerGetValuesResponse:
        """
        Retrieve the possible values of a shift layer

        Args:
          scheduler_id: The unique identifier of the scheduler

          layer_id: The unique identifier of the layer

          limit: The maximum number of results to display per page

          offset: The resource offset of the last successfully read resource will be returned as
              the paging.offset JSON property of a paginated response containing more results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not layer_id:
            raise ValueError(f"Expected a non-empty value for `layer_id` but received {layer_id!r}")
        return self._get(
            f"/scheduler/v1/schedulers/{scheduler_id}/shift-layers/{layer_id}/values",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                    },
                    shift_layer_get_values_params.ShiftLayerGetValuesParams,
                ),
            ),
            cast_to=ShiftLayerGetValuesResponse,
        )


class AsyncShiftLayersResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncShiftLayersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncShiftLayersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncShiftLayersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return AsyncShiftLayersResourceWithStreamingResponse(self)

    async def list(
        self,
        scheduler_id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ShiftLayerListResponse:
        """
        Retrieve a list of shift layers under a specified scheduler

        Args:
          scheduler_id: The unique identifier of the scheduler

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            f"/scheduler/v1/schedulers/{scheduler_id}/shift-layers",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ShiftLayerListResponse,
        )

    async def get_values(
        self,
        layer_id: str,
        *,
        scheduler_id: int,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ShiftLayerGetValuesResponse:
        """
        Retrieve the possible values of a shift layer

        Args:
          scheduler_id: The unique identifier of the scheduler

          layer_id: The unique identifier of the layer

          limit: The maximum number of results to display per page

          offset: The resource offset of the last successfully read resource will be returned as
              the paging.offset JSON property of a paginated response containing more results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not layer_id:
            raise ValueError(f"Expected a non-empty value for `layer_id` but received {layer_id!r}")
        return await self._get(
            f"/scheduler/v1/schedulers/{scheduler_id}/shift-layers/{layer_id}/values",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                    },
                    shift_layer_get_values_params.ShiftLayerGetValuesParams,
                ),
            ),
            cast_to=ShiftLayerGetValuesResponse,
        )


class ShiftLayersResourceWithRawResponse:
    def __init__(self, shift_layers: ShiftLayersResource) -> None:
        self._shift_layers = shift_layers

        self.list = to_raw_response_wrapper(
            shift_layers.list,
        )
        self.get_values = to_raw_response_wrapper(
            shift_layers.get_values,
        )


class AsyncShiftLayersResourceWithRawResponse:
    def __init__(self, shift_layers: AsyncShiftLayersResource) -> None:
        self._shift_layers = shift_layers

        self.list = async_to_raw_response_wrapper(
            shift_layers.list,
        )
        self.get_values = async_to_raw_response_wrapper(
            shift_layers.get_values,
        )


class ShiftLayersResourceWithStreamingResponse:
    def __init__(self, shift_layers: ShiftLayersResource) -> None:
        self._shift_layers = shift_layers

        self.list = to_streamed_response_wrapper(
            shift_layers.list,
        )
        self.get_values = to_streamed_response_wrapper(
            shift_layers.get_values,
        )


class AsyncShiftLayersResourceWithStreamingResponse:
    def __init__(self, shift_layers: AsyncShiftLayersResource) -> None:
        self._shift_layers = shift_layers

        self.list = async_to_streamed_response_wrapper(
            shift_layers.list,
        )
        self.get_values = async_to_streamed_response_wrapper(
            shift_layers.get_values,
        )
