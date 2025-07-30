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
from .time_activities import (
    TimeActivitiesResource,
    AsyncTimeActivitiesResource,
    TimeActivitiesResourceWithRawResponse,
    AsyncTimeActivitiesResourceWithRawResponse,
    TimeActivitiesResourceWithStreamingResponse,
    AsyncTimeActivitiesResourceWithStreamingResponse,
)
from ....._base_client import make_request_options
from .....types.time_clock.v1 import time_clock_clock_in_params, time_clock_clock_out_params
from .....types.time_clock.v1.gps_data_param import GpsDataParam
from .....types.time_clock.v1.time_clock_list_response import TimeClockListResponse
from .....types.time_clock.v1.time_clock_clock_in_response import TimeClockClockInResponse
from .....types.time_clock.v1.time_clock_clock_out_response import TimeClockClockOutResponse
from .....types.time_clock.v1.time_clock_get_manual_breaks_response import TimeClockGetManualBreaksResponse
from .....types.time_clock.v1.time_clock_get_shift_attachments_response import TimeClockGetShiftAttachmentsResponse

__all__ = ["TimeClocksResource", "AsyncTimeClocksResource"]


class TimeClocksResource(SyncAPIResource):
    @cached_property
    def time_activities(self) -> TimeActivitiesResource:
        return TimeActivitiesResource(self._client)

    @cached_property
    def with_raw_response(self) -> TimeClocksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return TimeClocksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TimeClocksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return TimeClocksResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TimeClockListResponse:
        """Retrieve a list of time clocks associated with the account"""
        return self._get(
            "/time-clock/v1/time-clocks",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TimeClockListResponse,
        )

    def clock_in(
        self,
        time_clock_id: int,
        *,
        job_id: str,
        user_id: int,
        location_data: GpsDataParam | NotGiven = NOT_GIVEN,
        scheduler_shift_id: str | NotGiven = NOT_GIVEN,
        timezone: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TimeClockClockInResponse:
        """Record the start time for the work period of an employee.

        The start time is
        automatically captured when the call is executed.

        Args:
          time_clock_id: The unique identifier of the time clock

          job_id: The unique identifier of the associated job or sub-job. Make sure the job is
              assigned to the specified time clock.

          user_id: The unique identifier of the user. Make sure the user is assigned to the
              specified time clock.

          location_data: GPS data associated with the clocking in event

          scheduler_shift_id: The scheduled shift from the job scheduler associated with the clocking in event

          timezone: The timezone in Tz format (e.g. America/New_York). If timezone is not specified,
              it will use the default timezone in the time clock settings.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            f"/time-clock/v1/time-clocks/{time_clock_id}/clock-in",
            body=maybe_transform(
                {
                    "job_id": job_id,
                    "user_id": user_id,
                    "location_data": location_data,
                    "scheduler_shift_id": scheduler_shift_id,
                    "timezone": timezone,
                },
                time_clock_clock_in_params.TimeClockClockInParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TimeClockClockInResponse,
        )

    def clock_out(
        self,
        time_clock_id: int,
        *,
        user_id: int,
        location_data: GpsDataParam | NotGiven = NOT_GIVEN,
        timezone: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TimeClockClockOutResponse:
        """Record the end time for the work period of an employee.

        The end time is
        automatically captured when the call is executed. The clock-out will be
        associated with the current open shift.

        Args:
          time_clock_id: The unique identifier of the time clock

          user_id: The unique identifier of the user. Make sure the user is assigned to the
              specified time clock.

          location_data: GPS data associated with the clocking out event

          timezone: The timezone in Tz format (e.g. America/New_York). If timezone is not specified,
              it will use the default timezone in the time clock settings.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            f"/time-clock/v1/time-clocks/{time_clock_id}/clock-out",
            body=maybe_transform(
                {
                    "user_id": user_id,
                    "location_data": location_data,
                    "timezone": timezone,
                },
                time_clock_clock_out_params.TimeClockClockOutParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TimeClockClockOutResponse,
        )

    def get_manual_breaks(
        self,
        time_clock_id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TimeClockGetManualBreaksResponse:
        """
        Get multiple manual breaks of a time clock

        Args:
          time_clock_id: The unique identifier of the time clock

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            f"/time-clock/v1/time-clocks/{time_clock_id}/manual-breaks",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TimeClockGetManualBreaksResponse,
        )

    def get_shift_attachments(
        self,
        time_clock_id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TimeClockGetShiftAttachmentsResponse:
        """
        Get shift attachments of a time clock

        Args:
          time_clock_id: The unique identifier of the time clock

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            f"/time-clock/v1/time-clocks/{time_clock_id}/shift-attachments",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TimeClockGetShiftAttachmentsResponse,
        )


class AsyncTimeClocksResource(AsyncAPIResource):
    @cached_property
    def time_activities(self) -> AsyncTimeActivitiesResource:
        return AsyncTimeActivitiesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncTimeClocksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTimeClocksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTimeClocksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return AsyncTimeClocksResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TimeClockListResponse:
        """Retrieve a list of time clocks associated with the account"""
        return await self._get(
            "/time-clock/v1/time-clocks",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TimeClockListResponse,
        )

    async def clock_in(
        self,
        time_clock_id: int,
        *,
        job_id: str,
        user_id: int,
        location_data: GpsDataParam | NotGiven = NOT_GIVEN,
        scheduler_shift_id: str | NotGiven = NOT_GIVEN,
        timezone: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TimeClockClockInResponse:
        """Record the start time for the work period of an employee.

        The start time is
        automatically captured when the call is executed.

        Args:
          time_clock_id: The unique identifier of the time clock

          job_id: The unique identifier of the associated job or sub-job. Make sure the job is
              assigned to the specified time clock.

          user_id: The unique identifier of the user. Make sure the user is assigned to the
              specified time clock.

          location_data: GPS data associated with the clocking in event

          scheduler_shift_id: The scheduled shift from the job scheduler associated with the clocking in event

          timezone: The timezone in Tz format (e.g. America/New_York). If timezone is not specified,
              it will use the default timezone in the time clock settings.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            f"/time-clock/v1/time-clocks/{time_clock_id}/clock-in",
            body=await async_maybe_transform(
                {
                    "job_id": job_id,
                    "user_id": user_id,
                    "location_data": location_data,
                    "scheduler_shift_id": scheduler_shift_id,
                    "timezone": timezone,
                },
                time_clock_clock_in_params.TimeClockClockInParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TimeClockClockInResponse,
        )

    async def clock_out(
        self,
        time_clock_id: int,
        *,
        user_id: int,
        location_data: GpsDataParam | NotGiven = NOT_GIVEN,
        timezone: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TimeClockClockOutResponse:
        """Record the end time for the work period of an employee.

        The end time is
        automatically captured when the call is executed. The clock-out will be
        associated with the current open shift.

        Args:
          time_clock_id: The unique identifier of the time clock

          user_id: The unique identifier of the user. Make sure the user is assigned to the
              specified time clock.

          location_data: GPS data associated with the clocking out event

          timezone: The timezone in Tz format (e.g. America/New_York). If timezone is not specified,
              it will use the default timezone in the time clock settings.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            f"/time-clock/v1/time-clocks/{time_clock_id}/clock-out",
            body=await async_maybe_transform(
                {
                    "user_id": user_id,
                    "location_data": location_data,
                    "timezone": timezone,
                },
                time_clock_clock_out_params.TimeClockClockOutParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TimeClockClockOutResponse,
        )

    async def get_manual_breaks(
        self,
        time_clock_id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TimeClockGetManualBreaksResponse:
        """
        Get multiple manual breaks of a time clock

        Args:
          time_clock_id: The unique identifier of the time clock

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            f"/time-clock/v1/time-clocks/{time_clock_id}/manual-breaks",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TimeClockGetManualBreaksResponse,
        )

    async def get_shift_attachments(
        self,
        time_clock_id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TimeClockGetShiftAttachmentsResponse:
        """
        Get shift attachments of a time clock

        Args:
          time_clock_id: The unique identifier of the time clock

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            f"/time-clock/v1/time-clocks/{time_clock_id}/shift-attachments",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TimeClockGetShiftAttachmentsResponse,
        )


class TimeClocksResourceWithRawResponse:
    def __init__(self, time_clocks: TimeClocksResource) -> None:
        self._time_clocks = time_clocks

        self.list = to_raw_response_wrapper(
            time_clocks.list,
        )
        self.clock_in = to_raw_response_wrapper(
            time_clocks.clock_in,
        )
        self.clock_out = to_raw_response_wrapper(
            time_clocks.clock_out,
        )
        self.get_manual_breaks = to_raw_response_wrapper(
            time_clocks.get_manual_breaks,
        )
        self.get_shift_attachments = to_raw_response_wrapper(
            time_clocks.get_shift_attachments,
        )

    @cached_property
    def time_activities(self) -> TimeActivitiesResourceWithRawResponse:
        return TimeActivitiesResourceWithRawResponse(self._time_clocks.time_activities)


class AsyncTimeClocksResourceWithRawResponse:
    def __init__(self, time_clocks: AsyncTimeClocksResource) -> None:
        self._time_clocks = time_clocks

        self.list = async_to_raw_response_wrapper(
            time_clocks.list,
        )
        self.clock_in = async_to_raw_response_wrapper(
            time_clocks.clock_in,
        )
        self.clock_out = async_to_raw_response_wrapper(
            time_clocks.clock_out,
        )
        self.get_manual_breaks = async_to_raw_response_wrapper(
            time_clocks.get_manual_breaks,
        )
        self.get_shift_attachments = async_to_raw_response_wrapper(
            time_clocks.get_shift_attachments,
        )

    @cached_property
    def time_activities(self) -> AsyncTimeActivitiesResourceWithRawResponse:
        return AsyncTimeActivitiesResourceWithRawResponse(self._time_clocks.time_activities)


class TimeClocksResourceWithStreamingResponse:
    def __init__(self, time_clocks: TimeClocksResource) -> None:
        self._time_clocks = time_clocks

        self.list = to_streamed_response_wrapper(
            time_clocks.list,
        )
        self.clock_in = to_streamed_response_wrapper(
            time_clocks.clock_in,
        )
        self.clock_out = to_streamed_response_wrapper(
            time_clocks.clock_out,
        )
        self.get_manual_breaks = to_streamed_response_wrapper(
            time_clocks.get_manual_breaks,
        )
        self.get_shift_attachments = to_streamed_response_wrapper(
            time_clocks.get_shift_attachments,
        )

    @cached_property
    def time_activities(self) -> TimeActivitiesResourceWithStreamingResponse:
        return TimeActivitiesResourceWithStreamingResponse(self._time_clocks.time_activities)


class AsyncTimeClocksResourceWithStreamingResponse:
    def __init__(self, time_clocks: AsyncTimeClocksResource) -> None:
        self._time_clocks = time_clocks

        self.list = async_to_streamed_response_wrapper(
            time_clocks.list,
        )
        self.clock_in = async_to_streamed_response_wrapper(
            time_clocks.clock_in,
        )
        self.clock_out = async_to_streamed_response_wrapper(
            time_clocks.clock_out,
        )
        self.get_manual_breaks = async_to_streamed_response_wrapper(
            time_clocks.get_manual_breaks,
        )
        self.get_shift_attachments = async_to_streamed_response_wrapper(
            time_clocks.get_shift_attachments,
        )

    @cached_property
    def time_activities(self) -> AsyncTimeActivitiesResourceWithStreamingResponse:
        return AsyncTimeActivitiesResourceWithStreamingResponse(self._time_clocks.time_activities)
