# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal

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
from .....types.time_clock.v1.time_clocks import (
    time_activity_list_params,
    time_activity_create_params,
    time_activity_update_params,
)
from .....types.time_clock.v1.time_clocks.time_activity_list_response import TimeActivityListResponse
from .....types.time_clock.v1.time_clocks.time_activity_create_response import TimeActivityCreateResponse
from .....types.time_clock.v1.time_clocks.time_activity_update_response import TimeActivityUpdateResponse

__all__ = ["TimeActivitiesResource", "AsyncTimeActivitiesResource"]


class TimeActivitiesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TimeActivitiesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return TimeActivitiesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TimeActivitiesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return TimeActivitiesResourceWithStreamingResponse(self)

    def create(
        self,
        time_clock_id: int,
        *,
        time_activities: Iterable[time_activity_create_params.TimeActivity],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TimeActivityCreateResponse:
        """
        Create multiple time activities in a time clock

        Args:
          time_clock_id: The unique identifier of the time clock

          time_activities: List of the time activities of the users

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            f"/time-clock/v1/time-clocks/{time_clock_id}/time-activities",
            body=maybe_transform(
                {"time_activities": time_activities}, time_activity_create_params.TimeActivityCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TimeActivityCreateResponse,
        )

    def update(
        self,
        time_clock_id: int,
        *,
        time_activities: Iterable[time_activity_update_params.TimeActivity],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TimeActivityUpdateResponse:
        """Update time activities for users assigned to a specific time clock.

        Time
        activities can include adjustments to shifts and/or manual breaks.

        Args:
          time_clock_id: The unique identifier of the time clock

          time_activities: List of time activities of the users

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._put(
            f"/time-clock/v1/time-clocks/{time_clock_id}/time-activities",
            body=maybe_transform(
                {"time_activities": time_activities}, time_activity_update_params.TimeActivityUpdateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TimeActivityUpdateResponse,
        )

    def list(
        self,
        time_clock_id: int,
        *,
        end_date: str,
        start_date: str,
        activity_types: List[Literal["shift", "manual_break", "time_off"]] | NotGiven = NOT_GIVEN,
        job_ids: List[str] | NotGiven = NOT_GIVEN,
        manual_break_ids: List[str] | NotGiven = NOT_GIVEN,
        policy_type_ids: List[str] | NotGiven = NOT_GIVEN,
        user_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TimeActivityListResponse:
        """Retrieve a list of time activities in under a specified time clock.

        Time
        activities include shift and/or manual breaks

        Args:
          time_clock_id: The unique identifier of the time clock

          end_date: The end time to filter by in ISO 8601 format (YYYY-MM-DD)

          start_date: The start time to filter by in ISO 8601 format (YYYY-MM-DD)

          activity_types: The time activity types: shift, manual_break or time_off

          job_ids: The job IDs of shifts

          manual_break_ids: The manual break IDs of manual breaks

          policy_type_ids: The policy type IDs of time offs

          user_ids: Filter time activities by a list of user IDs. Users who are no longer assigned
              to the specified time clock cannot be retrieved with this filter.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            f"/time-clock/v1/time-clocks/{time_clock_id}/time-activities",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "end_date": end_date,
                        "start_date": start_date,
                        "activity_types": activity_types,
                        "job_ids": job_ids,
                        "manual_break_ids": manual_break_ids,
                        "policy_type_ids": policy_type_ids,
                        "user_ids": user_ids,
                    },
                    time_activity_list_params.TimeActivityListParams,
                ),
            ),
            cast_to=TimeActivityListResponse,
        )


class AsyncTimeActivitiesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTimeActivitiesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTimeActivitiesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTimeActivitiesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return AsyncTimeActivitiesResourceWithStreamingResponse(self)

    async def create(
        self,
        time_clock_id: int,
        *,
        time_activities: Iterable[time_activity_create_params.TimeActivity],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TimeActivityCreateResponse:
        """
        Create multiple time activities in a time clock

        Args:
          time_clock_id: The unique identifier of the time clock

          time_activities: List of the time activities of the users

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            f"/time-clock/v1/time-clocks/{time_clock_id}/time-activities",
            body=await async_maybe_transform(
                {"time_activities": time_activities}, time_activity_create_params.TimeActivityCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TimeActivityCreateResponse,
        )

    async def update(
        self,
        time_clock_id: int,
        *,
        time_activities: Iterable[time_activity_update_params.TimeActivity],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TimeActivityUpdateResponse:
        """Update time activities for users assigned to a specific time clock.

        Time
        activities can include adjustments to shifts and/or manual breaks.

        Args:
          time_clock_id: The unique identifier of the time clock

          time_activities: List of time activities of the users

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._put(
            f"/time-clock/v1/time-clocks/{time_clock_id}/time-activities",
            body=await async_maybe_transform(
                {"time_activities": time_activities}, time_activity_update_params.TimeActivityUpdateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TimeActivityUpdateResponse,
        )

    async def list(
        self,
        time_clock_id: int,
        *,
        end_date: str,
        start_date: str,
        activity_types: List[Literal["shift", "manual_break", "time_off"]] | NotGiven = NOT_GIVEN,
        job_ids: List[str] | NotGiven = NOT_GIVEN,
        manual_break_ids: List[str] | NotGiven = NOT_GIVEN,
        policy_type_ids: List[str] | NotGiven = NOT_GIVEN,
        user_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TimeActivityListResponse:
        """Retrieve a list of time activities in under a specified time clock.

        Time
        activities include shift and/or manual breaks

        Args:
          time_clock_id: The unique identifier of the time clock

          end_date: The end time to filter by in ISO 8601 format (YYYY-MM-DD)

          start_date: The start time to filter by in ISO 8601 format (YYYY-MM-DD)

          activity_types: The time activity types: shift, manual_break or time_off

          job_ids: The job IDs of shifts

          manual_break_ids: The manual break IDs of manual breaks

          policy_type_ids: The policy type IDs of time offs

          user_ids: Filter time activities by a list of user IDs. Users who are no longer assigned
              to the specified time clock cannot be retrieved with this filter.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            f"/time-clock/v1/time-clocks/{time_clock_id}/time-activities",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "end_date": end_date,
                        "start_date": start_date,
                        "activity_types": activity_types,
                        "job_ids": job_ids,
                        "manual_break_ids": manual_break_ids,
                        "policy_type_ids": policy_type_ids,
                        "user_ids": user_ids,
                    },
                    time_activity_list_params.TimeActivityListParams,
                ),
            ),
            cast_to=TimeActivityListResponse,
        )


class TimeActivitiesResourceWithRawResponse:
    def __init__(self, time_activities: TimeActivitiesResource) -> None:
        self._time_activities = time_activities

        self.create = to_raw_response_wrapper(
            time_activities.create,
        )
        self.update = to_raw_response_wrapper(
            time_activities.update,
        )
        self.list = to_raw_response_wrapper(
            time_activities.list,
        )


class AsyncTimeActivitiesResourceWithRawResponse:
    def __init__(self, time_activities: AsyncTimeActivitiesResource) -> None:
        self._time_activities = time_activities

        self.create = async_to_raw_response_wrapper(
            time_activities.create,
        )
        self.update = async_to_raw_response_wrapper(
            time_activities.update,
        )
        self.list = async_to_raw_response_wrapper(
            time_activities.list,
        )


class TimeActivitiesResourceWithStreamingResponse:
    def __init__(self, time_activities: TimeActivitiesResource) -> None:
        self._time_activities = time_activities

        self.create = to_streamed_response_wrapper(
            time_activities.create,
        )
        self.update = to_streamed_response_wrapper(
            time_activities.update,
        )
        self.list = to_streamed_response_wrapper(
            time_activities.list,
        )


class AsyncTimeActivitiesResourceWithStreamingResponse:
    def __init__(self, time_activities: AsyncTimeActivitiesResource) -> None:
        self._time_activities = time_activities

        self.create = async_to_streamed_response_wrapper(
            time_activities.create,
        )
        self.update = async_to_streamed_response_wrapper(
            time_activities.update,
        )
        self.list = async_to_streamed_response_wrapper(
            time_activities.list,
        )
