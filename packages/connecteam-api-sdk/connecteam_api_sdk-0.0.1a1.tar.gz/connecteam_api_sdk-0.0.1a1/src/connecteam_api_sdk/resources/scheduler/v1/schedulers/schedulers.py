# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ....._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ....._utils import maybe_transform, async_maybe_transform
from ....._compat import cached_property
from .shift_layers import (
    ShiftLayersResource,
    AsyncShiftLayersResource,
    ShiftLayersResourceWithRawResponse,
    AsyncShiftLayersResourceWithRawResponse,
    ShiftLayersResourceWithStreamingResponse,
    AsyncShiftLayersResourceWithStreamingResponse,
)
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .shifts.shifts import (
    ShiftsResource,
    AsyncShiftsResource,
    ShiftsResourceWithRawResponse,
    AsyncShiftsResourceWithRawResponse,
    ShiftsResourceWithStreamingResponse,
    AsyncShiftsResourceWithStreamingResponse,
)
from ....._base_client import make_request_options
from .....types.scheduler.v1 import scheduler_get_user_unavailabilities_params
from .....types.scheduler.v1.scheduler_list_response import SchedulerListResponse
from .....types.scheduler.v1.scheduler_get_user_unavailabilities_response import (
    SchedulerGetUserUnavailabilitiesResponse,
)

__all__ = ["SchedulersResource", "AsyncSchedulersResource"]


class SchedulersResource(SyncAPIResource):
    @cached_property
    def shifts(self) -> ShiftsResource:
        return ShiftsResource(self._client)

    @cached_property
    def shift_layers(self) -> ShiftLayersResource:
        return ShiftLayersResource(self._client)

    @cached_property
    def with_raw_response(self) -> SchedulersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return SchedulersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SchedulersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return SchedulersResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SchedulerListResponse:
        """Retrieve a list of schedulers associated with the account"""
        return self._get(
            "/scheduler/v1/schedulers",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SchedulerListResponse,
        )

    def get_user_unavailabilities(
        self,
        *,
        end_time: int,
        start_time: int,
        user_id: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SchedulerGetUserUnavailabilitiesResponse:
        """
        Retrieve a list of user unavailabilities, approved time-off requests and
        assigned shifts

        Args:
          end_time: The end time to filter by in Unix format (in seconds)

          start_time: The start time to filter by in Unix format (in seconds)

          user_id: The unique identifier of the user

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/scheduler/v1/schedulers/user-unavailability",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "end_time": end_time,
                        "start_time": start_time,
                        "user_id": user_id,
                    },
                    scheduler_get_user_unavailabilities_params.SchedulerGetUserUnavailabilitiesParams,
                ),
            ),
            cast_to=SchedulerGetUserUnavailabilitiesResponse,
        )


class AsyncSchedulersResource(AsyncAPIResource):
    @cached_property
    def shifts(self) -> AsyncShiftsResource:
        return AsyncShiftsResource(self._client)

    @cached_property
    def shift_layers(self) -> AsyncShiftLayersResource:
        return AsyncShiftLayersResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncSchedulersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSchedulersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSchedulersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return AsyncSchedulersResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SchedulerListResponse:
        """Retrieve a list of schedulers associated with the account"""
        return await self._get(
            "/scheduler/v1/schedulers",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SchedulerListResponse,
        )

    async def get_user_unavailabilities(
        self,
        *,
        end_time: int,
        start_time: int,
        user_id: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SchedulerGetUserUnavailabilitiesResponse:
        """
        Retrieve a list of user unavailabilities, approved time-off requests and
        assigned shifts

        Args:
          end_time: The end time to filter by in Unix format (in seconds)

          start_time: The start time to filter by in Unix format (in seconds)

          user_id: The unique identifier of the user

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/scheduler/v1/schedulers/user-unavailability",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "end_time": end_time,
                        "start_time": start_time,
                        "user_id": user_id,
                    },
                    scheduler_get_user_unavailabilities_params.SchedulerGetUserUnavailabilitiesParams,
                ),
            ),
            cast_to=SchedulerGetUserUnavailabilitiesResponse,
        )


class SchedulersResourceWithRawResponse:
    def __init__(self, schedulers: SchedulersResource) -> None:
        self._schedulers = schedulers

        self.list = to_raw_response_wrapper(
            schedulers.list,
        )
        self.get_user_unavailabilities = to_raw_response_wrapper(
            schedulers.get_user_unavailabilities,
        )

    @cached_property
    def shifts(self) -> ShiftsResourceWithRawResponse:
        return ShiftsResourceWithRawResponse(self._schedulers.shifts)

    @cached_property
    def shift_layers(self) -> ShiftLayersResourceWithRawResponse:
        return ShiftLayersResourceWithRawResponse(self._schedulers.shift_layers)


class AsyncSchedulersResourceWithRawResponse:
    def __init__(self, schedulers: AsyncSchedulersResource) -> None:
        self._schedulers = schedulers

        self.list = async_to_raw_response_wrapper(
            schedulers.list,
        )
        self.get_user_unavailabilities = async_to_raw_response_wrapper(
            schedulers.get_user_unavailabilities,
        )

    @cached_property
    def shifts(self) -> AsyncShiftsResourceWithRawResponse:
        return AsyncShiftsResourceWithRawResponse(self._schedulers.shifts)

    @cached_property
    def shift_layers(self) -> AsyncShiftLayersResourceWithRawResponse:
        return AsyncShiftLayersResourceWithRawResponse(self._schedulers.shift_layers)


class SchedulersResourceWithStreamingResponse:
    def __init__(self, schedulers: SchedulersResource) -> None:
        self._schedulers = schedulers

        self.list = to_streamed_response_wrapper(
            schedulers.list,
        )
        self.get_user_unavailabilities = to_streamed_response_wrapper(
            schedulers.get_user_unavailabilities,
        )

    @cached_property
    def shifts(self) -> ShiftsResourceWithStreamingResponse:
        return ShiftsResourceWithStreamingResponse(self._schedulers.shifts)

    @cached_property
    def shift_layers(self) -> ShiftLayersResourceWithStreamingResponse:
        return ShiftLayersResourceWithStreamingResponse(self._schedulers.shift_layers)


class AsyncSchedulersResourceWithStreamingResponse:
    def __init__(self, schedulers: AsyncSchedulersResource) -> None:
        self._schedulers = schedulers

        self.list = async_to_streamed_response_wrapper(
            schedulers.list,
        )
        self.get_user_unavailabilities = async_to_streamed_response_wrapper(
            schedulers.get_user_unavailabilities,
        )

    @cached_property
    def shifts(self) -> AsyncShiftsResourceWithStreamingResponse:
        return AsyncShiftsResourceWithStreamingResponse(self._schedulers.shifts)

    @cached_property
    def shift_layers(self) -> AsyncShiftLayersResourceWithStreamingResponse:
        return AsyncShiftLayersResourceWithStreamingResponse(self._schedulers.shift_layers)
