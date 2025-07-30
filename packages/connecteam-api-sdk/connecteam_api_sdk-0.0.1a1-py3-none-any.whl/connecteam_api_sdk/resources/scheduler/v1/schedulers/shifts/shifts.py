# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal

import httpx

from ......_types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ......_utils import maybe_transform, async_maybe_transform
from .auto_assign import (
    AutoAssignResource,
    AsyncAutoAssignResource,
    AutoAssignResourceWithRawResponse,
    AsyncAutoAssignResourceWithRawResponse,
    AutoAssignResourceWithStreamingResponse,
    AsyncAutoAssignResourceWithStreamingResponse,
)
from ......_compat import cached_property
from ......_resource import SyncAPIResource, AsyncAPIResource
from ......_response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ......_base_client import make_request_options
from ......types.scheduler.v1.schedulers import (
    SortOrder,
    shift_list_params,
    shift_create_params,
    shift_delete_params,
    shift_update_params,
    shift_delete_shift_params,
)
from ......types.scheduler.v1.schedulers.sort_order import SortOrder
from ......types.scheduler.v1.schedulers.shift_list_response import ShiftListResponse
from ......types.scheduler.v1.schedulers.shift_delete_response import ShiftDeleteResponse
from ......types.scheduler.v1.schedulers.api_response_shift_bulk import APIResponseShiftBulk
from ......types.scheduler.v1.schedulers.shift_retrieve_response import ShiftRetrieveResponse
from ......types.scheduler.v1.schedulers.shift_delete_shift_response import ShiftDeleteShiftResponse

__all__ = ["ShiftsResource", "AsyncShiftsResource"]


class ShiftsResource(SyncAPIResource):
    @cached_property
    def auto_assign(self) -> AutoAssignResource:
        return AutoAssignResource(self._client)

    @cached_property
    def with_raw_response(self) -> ShiftsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return ShiftsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ShiftsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return ShiftsResourceWithStreamingResponse(self)

    def create(
        self,
        scheduler_id: int,
        *,
        body: Iterable[shift_create_params.Body],
        notify_users: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIResponseShiftBulk:
        """
        Create single or multiple shifts under a specific scheduler

        Args:
          scheduler_id: The unique identifier of the scheduler

          notify_users: Indicates whether to send a notification to the users assigned to the shifts.
              This applies only to shifts that are published.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            f"/scheduler/v1/schedulers/{scheduler_id}/shifts",
            body=maybe_transform(body, Iterable[shift_create_params.Body]),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"notify_users": notify_users}, shift_create_params.ShiftCreateParams),
            ),
            cast_to=APIResponseShiftBulk,
        )

    def retrieve(
        self,
        shift_id: str,
        *,
        scheduler_id: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ShiftRetrieveResponse:
        """
        Retrieve single shift information by its unique ID

        Args:
          scheduler_id: The unique identifier of the scheduler

          shift_id: The unique identifier of the shift

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not shift_id:
            raise ValueError(f"Expected a non-empty value for `shift_id` but received {shift_id!r}")
        return self._get(
            f"/scheduler/v1/schedulers/{scheduler_id}/shifts/{shift_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ShiftRetrieveResponse,
        )

    def update(
        self,
        scheduler_id: int,
        *,
        body: Iterable[shift_update_params.Body],
        notify_users: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIResponseShiftBulk:
        """
        Update single or multiple shifts under a specific scheduler

        Args:
          scheduler_id: The unique identifier of the scheduler

          notify_users: Indicates whether to send a notification to the users assigned to the shifts.
              This applies only to shifts that are published.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._put(
            f"/scheduler/v1/schedulers/{scheduler_id}/shifts",
            body=maybe_transform(body, Iterable[shift_update_params.Body]),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"notify_users": notify_users}, shift_update_params.ShiftUpdateParams),
            ),
            cast_to=APIResponseShiftBulk,
        )

    def list(
        self,
        scheduler_id: int,
        *,
        end_time: int,
        start_time: int,
        assigned_user_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        is_open_shift: bool | NotGiven = NOT_GIVEN,
        is_published: bool | NotGiven = NOT_GIVEN,
        is_require_admin_approval: bool | NotGiven = NOT_GIVEN,
        job_id: List[str] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        order: SortOrder | NotGiven = NOT_GIVEN,
        shift_id: List[str] | NotGiven = NOT_GIVEN,
        sort: Literal["created_at", "updated_at"] | NotGiven = NOT_GIVEN,
        title: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ShiftListResponse:
        """
        Retrieve a list of shifts under a specific scheduler

        Args:
          scheduler_id: The unique identifier of the scheduler

          end_time: The end time to filter by in Unix format (in seconds)

          start_time: The start time to filter by in Unix format (in seconds)

          assigned_user_ids: List of user IDs

          is_open_shift: Filter shifts that are open shifts

          is_published: Filter shifts that are published

          is_require_admin_approval: Filter shifts that require admin approval

          job_id: List of job IDs

          limit: The maximum number of results to display per page

          offset: The resource offset of the last successfully read resource will be returned as
              the paging.offset JSON property of a paginated response containing more results

          order: An enumeration.

          shift_id: List of shift IDs

          sort: An enumeration.

          title: Title of the shift

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            f"/scheduler/v1/schedulers/{scheduler_id}/shifts",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "end_time": end_time,
                        "start_time": start_time,
                        "assigned_user_ids": assigned_user_ids,
                        "is_open_shift": is_open_shift,
                        "is_published": is_published,
                        "is_require_admin_approval": is_require_admin_approval,
                        "job_id": job_id,
                        "limit": limit,
                        "offset": offset,
                        "order": order,
                        "shift_id": shift_id,
                        "sort": sort,
                        "title": title,
                    },
                    shift_list_params.ShiftListParams,
                ),
            ),
            cast_to=ShiftListResponse,
        )

    def delete(
        self,
        scheduler_id: int,
        *,
        shifts_ids: List[str],
        notify_users: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ShiftDeleteResponse:
        """
        Delete single or multiple shifts in a specified scheduler

        Args:
          scheduler_id: The unique identifier of the scheduler

          shifts_ids: The unique identifiers of the shifts to delete

          notify_users: Indicates whether to send a notification to the users assigned to the shifts.
              This applies only to shifts that are published.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._delete(
            f"/scheduler/v1/schedulers/{scheduler_id}/shifts",
            body=maybe_transform({"shifts_ids": shifts_ids}, shift_delete_params.ShiftDeleteParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"notify_users": notify_users}, shift_delete_params.ShiftDeleteParams),
            ),
            cast_to=ShiftDeleteResponse,
        )

    def delete_shift(
        self,
        shift_id: str,
        *,
        scheduler_id: int,
        notify_users: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ShiftDeleteShiftResponse:
        """
        Delete a single shift by its unique ID

        Args:
          scheduler_id: The unique identifier of the scheduler

          shift_id: The ID of the shift to delete

          notify_users: Indicates whether to send a notification to the users assigned to the shifts.
              This applies only to shifts that are published.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not shift_id:
            raise ValueError(f"Expected a non-empty value for `shift_id` but received {shift_id!r}")
        return self._delete(
            f"/scheduler/v1/schedulers/{scheduler_id}/shifts/{shift_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"notify_users": notify_users}, shift_delete_shift_params.ShiftDeleteShiftParams),
            ),
            cast_to=ShiftDeleteShiftResponse,
        )


class AsyncShiftsResource(AsyncAPIResource):
    @cached_property
    def auto_assign(self) -> AsyncAutoAssignResource:
        return AsyncAutoAssignResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncShiftsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncShiftsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncShiftsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return AsyncShiftsResourceWithStreamingResponse(self)

    async def create(
        self,
        scheduler_id: int,
        *,
        body: Iterable[shift_create_params.Body],
        notify_users: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIResponseShiftBulk:
        """
        Create single or multiple shifts under a specific scheduler

        Args:
          scheduler_id: The unique identifier of the scheduler

          notify_users: Indicates whether to send a notification to the users assigned to the shifts.
              This applies only to shifts that are published.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            f"/scheduler/v1/schedulers/{scheduler_id}/shifts",
            body=await async_maybe_transform(body, Iterable[shift_create_params.Body]),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"notify_users": notify_users}, shift_create_params.ShiftCreateParams
                ),
            ),
            cast_to=APIResponseShiftBulk,
        )

    async def retrieve(
        self,
        shift_id: str,
        *,
        scheduler_id: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ShiftRetrieveResponse:
        """
        Retrieve single shift information by its unique ID

        Args:
          scheduler_id: The unique identifier of the scheduler

          shift_id: The unique identifier of the shift

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not shift_id:
            raise ValueError(f"Expected a non-empty value for `shift_id` but received {shift_id!r}")
        return await self._get(
            f"/scheduler/v1/schedulers/{scheduler_id}/shifts/{shift_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ShiftRetrieveResponse,
        )

    async def update(
        self,
        scheduler_id: int,
        *,
        body: Iterable[shift_update_params.Body],
        notify_users: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIResponseShiftBulk:
        """
        Update single or multiple shifts under a specific scheduler

        Args:
          scheduler_id: The unique identifier of the scheduler

          notify_users: Indicates whether to send a notification to the users assigned to the shifts.
              This applies only to shifts that are published.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._put(
            f"/scheduler/v1/schedulers/{scheduler_id}/shifts",
            body=await async_maybe_transform(body, Iterable[shift_update_params.Body]),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"notify_users": notify_users}, shift_update_params.ShiftUpdateParams
                ),
            ),
            cast_to=APIResponseShiftBulk,
        )

    async def list(
        self,
        scheduler_id: int,
        *,
        end_time: int,
        start_time: int,
        assigned_user_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        is_open_shift: bool | NotGiven = NOT_GIVEN,
        is_published: bool | NotGiven = NOT_GIVEN,
        is_require_admin_approval: bool | NotGiven = NOT_GIVEN,
        job_id: List[str] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        order: SortOrder | NotGiven = NOT_GIVEN,
        shift_id: List[str] | NotGiven = NOT_GIVEN,
        sort: Literal["created_at", "updated_at"] | NotGiven = NOT_GIVEN,
        title: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ShiftListResponse:
        """
        Retrieve a list of shifts under a specific scheduler

        Args:
          scheduler_id: The unique identifier of the scheduler

          end_time: The end time to filter by in Unix format (in seconds)

          start_time: The start time to filter by in Unix format (in seconds)

          assigned_user_ids: List of user IDs

          is_open_shift: Filter shifts that are open shifts

          is_published: Filter shifts that are published

          is_require_admin_approval: Filter shifts that require admin approval

          job_id: List of job IDs

          limit: The maximum number of results to display per page

          offset: The resource offset of the last successfully read resource will be returned as
              the paging.offset JSON property of a paginated response containing more results

          order: An enumeration.

          shift_id: List of shift IDs

          sort: An enumeration.

          title: Title of the shift

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            f"/scheduler/v1/schedulers/{scheduler_id}/shifts",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "end_time": end_time,
                        "start_time": start_time,
                        "assigned_user_ids": assigned_user_ids,
                        "is_open_shift": is_open_shift,
                        "is_published": is_published,
                        "is_require_admin_approval": is_require_admin_approval,
                        "job_id": job_id,
                        "limit": limit,
                        "offset": offset,
                        "order": order,
                        "shift_id": shift_id,
                        "sort": sort,
                        "title": title,
                    },
                    shift_list_params.ShiftListParams,
                ),
            ),
            cast_to=ShiftListResponse,
        )

    async def delete(
        self,
        scheduler_id: int,
        *,
        shifts_ids: List[str],
        notify_users: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ShiftDeleteResponse:
        """
        Delete single or multiple shifts in a specified scheduler

        Args:
          scheduler_id: The unique identifier of the scheduler

          shifts_ids: The unique identifiers of the shifts to delete

          notify_users: Indicates whether to send a notification to the users assigned to the shifts.
              This applies only to shifts that are published.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._delete(
            f"/scheduler/v1/schedulers/{scheduler_id}/shifts",
            body=await async_maybe_transform({"shifts_ids": shifts_ids}, shift_delete_params.ShiftDeleteParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"notify_users": notify_users}, shift_delete_params.ShiftDeleteParams
                ),
            ),
            cast_to=ShiftDeleteResponse,
        )

    async def delete_shift(
        self,
        shift_id: str,
        *,
        scheduler_id: int,
        notify_users: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ShiftDeleteShiftResponse:
        """
        Delete a single shift by its unique ID

        Args:
          scheduler_id: The unique identifier of the scheduler

          shift_id: The ID of the shift to delete

          notify_users: Indicates whether to send a notification to the users assigned to the shifts.
              This applies only to shifts that are published.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not shift_id:
            raise ValueError(f"Expected a non-empty value for `shift_id` but received {shift_id!r}")
        return await self._delete(
            f"/scheduler/v1/schedulers/{scheduler_id}/shifts/{shift_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"notify_users": notify_users}, shift_delete_shift_params.ShiftDeleteShiftParams
                ),
            ),
            cast_to=ShiftDeleteShiftResponse,
        )


class ShiftsResourceWithRawResponse:
    def __init__(self, shifts: ShiftsResource) -> None:
        self._shifts = shifts

        self.create = to_raw_response_wrapper(
            shifts.create,
        )
        self.retrieve = to_raw_response_wrapper(
            shifts.retrieve,
        )
        self.update = to_raw_response_wrapper(
            shifts.update,
        )
        self.list = to_raw_response_wrapper(
            shifts.list,
        )
        self.delete = to_raw_response_wrapper(
            shifts.delete,
        )
        self.delete_shift = to_raw_response_wrapper(
            shifts.delete_shift,
        )

    @cached_property
    def auto_assign(self) -> AutoAssignResourceWithRawResponse:
        return AutoAssignResourceWithRawResponse(self._shifts.auto_assign)


class AsyncShiftsResourceWithRawResponse:
    def __init__(self, shifts: AsyncShiftsResource) -> None:
        self._shifts = shifts

        self.create = async_to_raw_response_wrapper(
            shifts.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            shifts.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            shifts.update,
        )
        self.list = async_to_raw_response_wrapper(
            shifts.list,
        )
        self.delete = async_to_raw_response_wrapper(
            shifts.delete,
        )
        self.delete_shift = async_to_raw_response_wrapper(
            shifts.delete_shift,
        )

    @cached_property
    def auto_assign(self) -> AsyncAutoAssignResourceWithRawResponse:
        return AsyncAutoAssignResourceWithRawResponse(self._shifts.auto_assign)


class ShiftsResourceWithStreamingResponse:
    def __init__(self, shifts: ShiftsResource) -> None:
        self._shifts = shifts

        self.create = to_streamed_response_wrapper(
            shifts.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            shifts.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            shifts.update,
        )
        self.list = to_streamed_response_wrapper(
            shifts.list,
        )
        self.delete = to_streamed_response_wrapper(
            shifts.delete,
        )
        self.delete_shift = to_streamed_response_wrapper(
            shifts.delete_shift,
        )

    @cached_property
    def auto_assign(self) -> AutoAssignResourceWithStreamingResponse:
        return AutoAssignResourceWithStreamingResponse(self._shifts.auto_assign)


class AsyncShiftsResourceWithStreamingResponse:
    def __init__(self, shifts: AsyncShiftsResource) -> None:
        self._shifts = shifts

        self.create = async_to_streamed_response_wrapper(
            shifts.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            shifts.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            shifts.update,
        )
        self.list = async_to_streamed_response_wrapper(
            shifts.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            shifts.delete,
        )
        self.delete_shift = async_to_streamed_response_wrapper(
            shifts.delete_shift,
        )

    @cached_property
    def auto_assign(self) -> AsyncAutoAssignResourceWithStreamingResponse:
        return AsyncAutoAssignResourceWithStreamingResponse(self._shifts.auto_assign)
