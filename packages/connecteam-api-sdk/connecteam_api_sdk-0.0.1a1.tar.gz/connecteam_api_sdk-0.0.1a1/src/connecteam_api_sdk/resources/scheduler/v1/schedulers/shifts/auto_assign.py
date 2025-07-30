# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List

import httpx

from ......_types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ......_utils import maybe_transform, async_maybe_transform
from ......_compat import cached_property
from ......_resource import SyncAPIResource, AsyncAPIResource
from ......_response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ......_base_client import make_request_options
from ......types.scheduler.v1.schedulers.shifts import auto_assign_create_request_params
from ......types.scheduler.v1.schedulers.shifts.auto_assign_get_status_response import AutoAssignGetStatusResponse
from ......types.scheduler.v1.schedulers.shifts.auto_assign_create_request_response import (
    AutoAssignCreateRequestResponse,
)

__all__ = ["AutoAssignResource", "AsyncAutoAssignResource"]


class AutoAssignResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AutoAssignResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AutoAssignResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AutoAssignResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return AutoAssignResourceWithStreamingResponse(self)

    def create_request(
        self,
        scheduler_id: int,
        *,
        shifts_ids: List[str],
        is_force_limitations: bool | NotGiven = NOT_GIVEN,
        is_force_open_shift_requests: bool | NotGiven = NOT_GIVEN,
        is_force_qualification: bool | NotGiven = NOT_GIVEN,
        is_force_unavailability: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AutoAssignCreateRequestResponse:
        """Initiate a request to auto-assign shifts by their IDs.

        If multiple IDs are
        provided, all corresponding shifts must occur within the same work week (e.g.,
        Monday to Sunday). This endpoint only submits the request; processing may take a
        few minutes. The auto-assignment considers user preferences to work,
        unavailability, and approved time off. For assignment status, refer to the
        auto-assign status endpoint.

        Args:
          scheduler_id: The unique identifier of the scheduler

          shifts_ids: List of shift IDs to start a request to auto assign. The shifts must be within
              the same week period (according to the scheduler settings).

          is_force_limitations: Determines whether to consider users' limitations.

          is_force_open_shift_requests: Determines whether to assign open shifts exclusively to requesters. If set to
              false, it first prioritizes requesters, then assigns the remaining.

          is_force_qualification: Determines whether to take into consideration the qualifications of users.

          is_force_unavailability: Determines whether to consider users' unavailabilities.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            f"/scheduler/v1/schedulers/{scheduler_id}/shifts/auto-assign",
            body=maybe_transform(
                {
                    "shifts_ids": shifts_ids,
                    "is_force_limitations": is_force_limitations,
                    "is_force_open_shift_requests": is_force_open_shift_requests,
                    "is_force_qualification": is_force_qualification,
                    "is_force_unavailability": is_force_unavailability,
                },
                auto_assign_create_request_params.AutoAssignCreateRequestParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AutoAssignCreateRequestResponse,
        )

    def get_status(
        self,
        auto_assign_request_id: int,
        *,
        scheduler_id: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AutoAssignGetStatusResponse:
        """Retrieve the status of an auto-assign request using its unique request ID.

        The
        response categorizes the results into 'scheduled shifts' for successfully
        assigned shifts and 'unscheduled shifts' for those where auto-assignment was not
        successful.

        Args:
          scheduler_id: The unique identifier of the scheduler

          auto_assign_request_id: The unique identifier of the auto assign request

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            f"/scheduler/v1/schedulers/{scheduler_id}/shifts/auto-assign/{auto_assign_request_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AutoAssignGetStatusResponse,
        )


class AsyncAutoAssignResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAutoAssignResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAutoAssignResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAutoAssignResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return AsyncAutoAssignResourceWithStreamingResponse(self)

    async def create_request(
        self,
        scheduler_id: int,
        *,
        shifts_ids: List[str],
        is_force_limitations: bool | NotGiven = NOT_GIVEN,
        is_force_open_shift_requests: bool | NotGiven = NOT_GIVEN,
        is_force_qualification: bool | NotGiven = NOT_GIVEN,
        is_force_unavailability: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AutoAssignCreateRequestResponse:
        """Initiate a request to auto-assign shifts by their IDs.

        If multiple IDs are
        provided, all corresponding shifts must occur within the same work week (e.g.,
        Monday to Sunday). This endpoint only submits the request; processing may take a
        few minutes. The auto-assignment considers user preferences to work,
        unavailability, and approved time off. For assignment status, refer to the
        auto-assign status endpoint.

        Args:
          scheduler_id: The unique identifier of the scheduler

          shifts_ids: List of shift IDs to start a request to auto assign. The shifts must be within
              the same week period (according to the scheduler settings).

          is_force_limitations: Determines whether to consider users' limitations.

          is_force_open_shift_requests: Determines whether to assign open shifts exclusively to requesters. If set to
              false, it first prioritizes requesters, then assigns the remaining.

          is_force_qualification: Determines whether to take into consideration the qualifications of users.

          is_force_unavailability: Determines whether to consider users' unavailabilities.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            f"/scheduler/v1/schedulers/{scheduler_id}/shifts/auto-assign",
            body=await async_maybe_transform(
                {
                    "shifts_ids": shifts_ids,
                    "is_force_limitations": is_force_limitations,
                    "is_force_open_shift_requests": is_force_open_shift_requests,
                    "is_force_qualification": is_force_qualification,
                    "is_force_unavailability": is_force_unavailability,
                },
                auto_assign_create_request_params.AutoAssignCreateRequestParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AutoAssignCreateRequestResponse,
        )

    async def get_status(
        self,
        auto_assign_request_id: int,
        *,
        scheduler_id: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AutoAssignGetStatusResponse:
        """Retrieve the status of an auto-assign request using its unique request ID.

        The
        response categorizes the results into 'scheduled shifts' for successfully
        assigned shifts and 'unscheduled shifts' for those where auto-assignment was not
        successful.

        Args:
          scheduler_id: The unique identifier of the scheduler

          auto_assign_request_id: The unique identifier of the auto assign request

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            f"/scheduler/v1/schedulers/{scheduler_id}/shifts/auto-assign/{auto_assign_request_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AutoAssignGetStatusResponse,
        )


class AutoAssignResourceWithRawResponse:
    def __init__(self, auto_assign: AutoAssignResource) -> None:
        self._auto_assign = auto_assign

        self.create_request = to_raw_response_wrapper(
            auto_assign.create_request,
        )
        self.get_status = to_raw_response_wrapper(
            auto_assign.get_status,
        )


class AsyncAutoAssignResourceWithRawResponse:
    def __init__(self, auto_assign: AsyncAutoAssignResource) -> None:
        self._auto_assign = auto_assign

        self.create_request = async_to_raw_response_wrapper(
            auto_assign.create_request,
        )
        self.get_status = async_to_raw_response_wrapper(
            auto_assign.get_status,
        )


class AutoAssignResourceWithStreamingResponse:
    def __init__(self, auto_assign: AutoAssignResource) -> None:
        self._auto_assign = auto_assign

        self.create_request = to_streamed_response_wrapper(
            auto_assign.create_request,
        )
        self.get_status = to_streamed_response_wrapper(
            auto_assign.get_status,
        )


class AsyncAutoAssignResourceWithStreamingResponse:
    def __init__(self, auto_assign: AsyncAutoAssignResource) -> None:
        self._auto_assign = auto_assign

        self.create_request = async_to_streamed_response_wrapper(
            auto_assign.create_request,
        )
        self.get_status = async_to_streamed_response_wrapper(
            auto_assign.get_status,
        )
