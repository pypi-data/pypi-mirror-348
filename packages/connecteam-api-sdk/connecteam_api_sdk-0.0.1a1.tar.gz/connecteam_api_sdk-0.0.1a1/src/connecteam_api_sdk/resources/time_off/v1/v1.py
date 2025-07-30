# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

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
from ....types.time_off import v1_create_request_params
from .policy_types.policy_types import (
    PolicyTypesResource,
    AsyncPolicyTypesResource,
    PolicyTypesResourceWithRawResponse,
    AsyncPolicyTypesResourceWithRawResponse,
    PolicyTypesResourceWithStreamingResponse,
    AsyncPolicyTypesResourceWithStreamingResponse,
)
from ....types.time_off.v1_create_request_response import V1CreateRequestResponse

__all__ = ["V1Resource", "AsyncV1Resource"]


class V1Resource(SyncAPIResource):
    @cached_property
    def policy_types(self) -> PolicyTypesResource:
        return PolicyTypesResource(self._client)

    @cached_property
    def with_raw_response(self) -> V1ResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return V1ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> V1ResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return V1ResourceWithStreamingResponse(self)

    def create_request(
        self,
        *,
        end_date: str,
        is_all_day: bool,
        policy_type_id: str,
        start_date: str,
        status: Literal["approved", "pending", "denied"],
        timezone: str,
        user_id: int,
        employee_note: str | NotGiven = NOT_GIVEN,
        end_time: str | NotGiven = NOT_GIVEN,
        is_adjust_for_day_light_saving: bool | NotGiven = NOT_GIVEN,
        manager_note: str | NotGiven = NOT_GIVEN,
        start_time: str | NotGiven = NOT_GIVEN,
        time_clock_id: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> V1CreateRequestResponse:
        """Create a new time-off request for a user under a specified policy.

        The time-off
        request can be either in pending or approved status.

        Args:
          end_date: The end time of the time off in ISO format (YYYY-MM-DD). End date must be
              similar to Start date if isAllDay set to false.

          is_all_day: Specifies the type of the time period. Defaults to true. If set to false, start
              and end time fields must be specified.

          policy_type_id: The ID of the policy type

          start_date: The start date of the time off in ISO format (YYYY-MM-DD)

          status: The status of the time off request.

          timezone: The timezone in Tz format (e.g. America/New_York)

          user_id: The ID of the user to create the time off request

          employee_note: Employee note providing additional details

          end_time: The end time of the time off in ISO format (HH:MM:SS). This field is required if
              isAllDay set to false.

          is_adjust_for_day_light_saving: Specifies if the time given should offset the daylight savings time change if
              the time falls exactly on the daylight savings time change. Set to true only if
              the time coincides with the rollback hour, otherwise, it should remain false.

          manager_note: Manager note providing additional details

          start_time: The start time of the time off in ISO format (HH:MM:SS). This field is required
              if isAllDay set to false.

          time_clock_id: The unique identifier of the time clock where the time off will be presented in
              the timesheet

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/time-off/v1/requests",
            body=maybe_transform(
                {
                    "end_date": end_date,
                    "is_all_day": is_all_day,
                    "policy_type_id": policy_type_id,
                    "start_date": start_date,
                    "status": status,
                    "timezone": timezone,
                    "user_id": user_id,
                    "employee_note": employee_note,
                    "end_time": end_time,
                    "is_adjust_for_day_light_saving": is_adjust_for_day_light_saving,
                    "manager_note": manager_note,
                    "start_time": start_time,
                    "time_clock_id": time_clock_id,
                },
                v1_create_request_params.V1CreateRequestParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1CreateRequestResponse,
        )


class AsyncV1Resource(AsyncAPIResource):
    @cached_property
    def policy_types(self) -> AsyncPolicyTypesResource:
        return AsyncPolicyTypesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncV1ResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncV1ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncV1ResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return AsyncV1ResourceWithStreamingResponse(self)

    async def create_request(
        self,
        *,
        end_date: str,
        is_all_day: bool,
        policy_type_id: str,
        start_date: str,
        status: Literal["approved", "pending", "denied"],
        timezone: str,
        user_id: int,
        employee_note: str | NotGiven = NOT_GIVEN,
        end_time: str | NotGiven = NOT_GIVEN,
        is_adjust_for_day_light_saving: bool | NotGiven = NOT_GIVEN,
        manager_note: str | NotGiven = NOT_GIVEN,
        start_time: str | NotGiven = NOT_GIVEN,
        time_clock_id: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> V1CreateRequestResponse:
        """Create a new time-off request for a user under a specified policy.

        The time-off
        request can be either in pending or approved status.

        Args:
          end_date: The end time of the time off in ISO format (YYYY-MM-DD). End date must be
              similar to Start date if isAllDay set to false.

          is_all_day: Specifies the type of the time period. Defaults to true. If set to false, start
              and end time fields must be specified.

          policy_type_id: The ID of the policy type

          start_date: The start date of the time off in ISO format (YYYY-MM-DD)

          status: The status of the time off request.

          timezone: The timezone in Tz format (e.g. America/New_York)

          user_id: The ID of the user to create the time off request

          employee_note: Employee note providing additional details

          end_time: The end time of the time off in ISO format (HH:MM:SS). This field is required if
              isAllDay set to false.

          is_adjust_for_day_light_saving: Specifies if the time given should offset the daylight savings time change if
              the time falls exactly on the daylight savings time change. Set to true only if
              the time coincides with the rollback hour, otherwise, it should remain false.

          manager_note: Manager note providing additional details

          start_time: The start time of the time off in ISO format (HH:MM:SS). This field is required
              if isAllDay set to false.

          time_clock_id: The unique identifier of the time clock where the time off will be presented in
              the timesheet

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/time-off/v1/requests",
            body=await async_maybe_transform(
                {
                    "end_date": end_date,
                    "is_all_day": is_all_day,
                    "policy_type_id": policy_type_id,
                    "start_date": start_date,
                    "status": status,
                    "timezone": timezone,
                    "user_id": user_id,
                    "employee_note": employee_note,
                    "end_time": end_time,
                    "is_adjust_for_day_light_saving": is_adjust_for_day_light_saving,
                    "manager_note": manager_note,
                    "start_time": start_time,
                    "time_clock_id": time_clock_id,
                },
                v1_create_request_params.V1CreateRequestParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V1CreateRequestResponse,
        )


class V1ResourceWithRawResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

        self.create_request = to_raw_response_wrapper(
            v1.create_request,
        )

    @cached_property
    def policy_types(self) -> PolicyTypesResourceWithRawResponse:
        return PolicyTypesResourceWithRawResponse(self._v1.policy_types)


class AsyncV1ResourceWithRawResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

        self.create_request = async_to_raw_response_wrapper(
            v1.create_request,
        )

    @cached_property
    def policy_types(self) -> AsyncPolicyTypesResourceWithRawResponse:
        return AsyncPolicyTypesResourceWithRawResponse(self._v1.policy_types)


class V1ResourceWithStreamingResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

        self.create_request = to_streamed_response_wrapper(
            v1.create_request,
        )

    @cached_property
    def policy_types(self) -> PolicyTypesResourceWithStreamingResponse:
        return PolicyTypesResourceWithStreamingResponse(self._v1.policy_types)


class AsyncV1ResourceWithStreamingResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

        self.create_request = async_to_streamed_response_wrapper(
            v1.create_request,
        )

    @cached_property
    def policy_types(self) -> AsyncPolicyTypesResourceWithStreamingResponse:
        return AsyncPolicyTypesResourceWithStreamingResponse(self._v1.policy_types)
