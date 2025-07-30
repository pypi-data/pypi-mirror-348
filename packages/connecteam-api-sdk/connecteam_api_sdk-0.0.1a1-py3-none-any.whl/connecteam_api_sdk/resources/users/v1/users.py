# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable
from datetime import date
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
from ....types.users.v1 import (
    user_list_params,
    user_create_params,
    user_update_params,
    user_create_note_params,
    user_upload_payslip_params,
    user_update_performance_params,
)
from ....types.scheduler.v1.schedulers import SortOrder
from ....types.users.v1.user_list_response import UserListResponse
from ....types.users.v1.user_create_response import UserCreateResponse
from ....types.users.v1.user_update_response import UserUpdateResponse
from ....types.users.v1.user_archive_response import UserArchiveResponse
from ....types.scheduler.v1.schedulers.sort_order import SortOrder
from ....types.users.v1.user_create_note_response import UserCreateNoteResponse
from ....types.users.v1.custom_fields.api_response_base import APIResponseBase
from ....types.users.v1.user_update_performance_response import UserUpdatePerformanceResponse

__all__ = ["UsersResource", "AsyncUsersResource"]


class UsersResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> UsersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return UsersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> UsersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return UsersResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        body: Iterable[user_create_params.Body],
        send_activation: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UserCreateResponse:
        """
        Create individual or multiple users associated with the account using the
        provided details.

        Args:
          body: List of users to create.

          send_activation: Optional flag to send activation sms.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/users/v1/users",
            body=maybe_transform(body, Iterable[user_create_params.Body]),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"send_activation": send_activation}, user_create_params.UserCreateParams),
            ),
            cast_to=UserCreateResponse,
        )

    def update(
        self,
        *,
        body: Iterable[user_update_params.Body],
        edit_users_by_phone: bool | NotGiven = NOT_GIVEN,
        include_smart_group_ids: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UserUpdateResponse:
        """
        Update individual or multiple users associated with the account using the
        provided details. You can specify updates either by their phone number or unique
        userID.

        Args:
          body: List of users to edit.

          edit_users_by_phone: Optional flag to edit users by phone (default by user id).

          include_smart_group_ids: Indicates whether to include smart group IDs in the response body for the
              updated user(s). Please note that setting this value to true may increase the
              request time significantly.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._put(
            "/users/v1/users",
            body=maybe_transform(body, Iterable[user_update_params.Body]),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "edit_users_by_phone": edit_users_by_phone,
                        "include_smart_group_ids": include_smart_group_ids,
                    },
                    user_update_params.UserUpdateParams,
                ),
            ),
            cast_to=UserUpdateResponse,
        )

    def list(
        self,
        *,
        created_at: int | NotGiven = NOT_GIVEN,
        email_addresses: List[str] | NotGiven = NOT_GIVEN,
        full_names: List[str] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        modified_at: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        order: SortOrder | NotGiven = NOT_GIVEN,
        phone_numbers: List[str] | NotGiven = NOT_GIVEN,
        sort: Literal["created_at"] | NotGiven = NOT_GIVEN,
        user_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        user_status: Literal["active", "archived", "all"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UserListResponse:
        """Retrieves a list of all users associated with the account.

        Optionally, filter by
        user ID to receive specific user information

        Args:
          created_at: Parameter specifying the date in Unix format (in seconds). Only users created
              after this date will be included in the results.

          email_addresses: List of email addresses to filter by (in format test@test.com).

          full_names: List of full names to filter by. Specify the exact first and last name with a
              space between them as shown in the platform (ignore capitalization).

          limit: The maximum number of results to display per page

          modified_at: Parameter specifying the date in in Unix format (in seconds). Only users with
              fields updated after this date will be included in the results.

          offset: The resource offset of the last successfully read resource will be returned as
              the paging.offset JSON property of a paginated response containing more results

          order: An enumeration.

          phone_numbers: List of phone numbers to filter by (in format +<country code><phone number>).

          sort: An enumeration.

          user_ids: List of user IDs for filtering.

          user_status: An enumeration.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/users/v1/users",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "created_at": created_at,
                        "email_addresses": email_addresses,
                        "full_names": full_names,
                        "limit": limit,
                        "modified_at": modified_at,
                        "offset": offset,
                        "order": order,
                        "phone_numbers": phone_numbers,
                        "sort": sort,
                        "user_ids": user_ids,
                        "user_status": user_status,
                    },
                    user_list_params.UserListParams,
                ),
            ),
            cast_to=UserListResponse,
        )

    def archive(
        self,
        *,
        body: Iterable[int],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UserArchiveResponse:
        """
        Archive individual or multiple users associated with the account by their unique
        userID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._delete(
            "/users/v1/users",
            body=maybe_transform(body, Iterable[int]),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UserArchiveResponse,
        )

    def create_note(
        self,
        user_id: int,
        *,
        text: str,
        title: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UserCreateNoteResponse:
        """
        Create new note on the profile of the specified user

        Args:
          user_id: The unique identifier of user to create note for

          text: The text of the user note to be created

          title: The title of the user note to be created

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            f"/users/v1/users/{user_id}/notes",
            body=maybe_transform(
                {
                    "text": text,
                    "title": title,
                },
                user_create_note_params.UserCreateNoteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UserCreateNoteResponse,
        )

    def update_performance(
        self,
        date: Union[str, date],
        *,
        user_id: int,
        items: Iterable[user_update_performance_params.Item],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UserUpdatePerformanceResponse:
        """Update or add performance data values for a specific user on a given date.

        If a
        value already exists for that date, it will be replaced with the new value. If
        no value exists, the new value will be added.

        Args:
          user_id: The ID of the user whose data is being accessed or modified

          date: The date to which the value(s) will be added, specified in ISO 8601 format
              (e.g., 2025-01-25)

          items: List of performance data values to update

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not date:
            raise ValueError(f"Expected a non-empty value for `date` but received {date!r}")
        return self._put(
            f"/users/v1/users/{user_id}/performance/{date}",
            body=maybe_transform({"items": items}, user_update_performance_params.UserUpdatePerformanceParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UserUpdatePerformanceResponse,
        )

    def upload_payslip(
        self,
        user_id: int,
        *,
        end_date: str,
        file_id: str,
        start_date: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIResponseBase:
        """Upload a payslip for a user for a specified period.

        The payslip attachment must
        be uploaded first via the attachments endpoint.

        Args:
          user_id: The unique identifier of the user

          end_date: The end date for the payslip in ISO 8601 format (YYYY-MM-DD)

          file_id: The unique identifier of the payslip attachment

          start_date: The start date for the payslip in ISO 8601 format (YYYY-MM-DD)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            f"/users/v1/users/{user_id}/payslips",
            body=maybe_transform(
                {
                    "end_date": end_date,
                    "file_id": file_id,
                    "start_date": start_date,
                },
                user_upload_payslip_params.UserUploadPayslipParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIResponseBase,
        )


class AsyncUsersResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncUsersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncUsersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncUsersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return AsyncUsersResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        body: Iterable[user_create_params.Body],
        send_activation: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UserCreateResponse:
        """
        Create individual or multiple users associated with the account using the
        provided details.

        Args:
          body: List of users to create.

          send_activation: Optional flag to send activation sms.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/users/v1/users",
            body=await async_maybe_transform(body, Iterable[user_create_params.Body]),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"send_activation": send_activation}, user_create_params.UserCreateParams
                ),
            ),
            cast_to=UserCreateResponse,
        )

    async def update(
        self,
        *,
        body: Iterable[user_update_params.Body],
        edit_users_by_phone: bool | NotGiven = NOT_GIVEN,
        include_smart_group_ids: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UserUpdateResponse:
        """
        Update individual or multiple users associated with the account using the
        provided details. You can specify updates either by their phone number or unique
        userID.

        Args:
          body: List of users to edit.

          edit_users_by_phone: Optional flag to edit users by phone (default by user id).

          include_smart_group_ids: Indicates whether to include smart group IDs in the response body for the
              updated user(s). Please note that setting this value to true may increase the
              request time significantly.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._put(
            "/users/v1/users",
            body=await async_maybe_transform(body, Iterable[user_update_params.Body]),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "edit_users_by_phone": edit_users_by_phone,
                        "include_smart_group_ids": include_smart_group_ids,
                    },
                    user_update_params.UserUpdateParams,
                ),
            ),
            cast_to=UserUpdateResponse,
        )

    async def list(
        self,
        *,
        created_at: int | NotGiven = NOT_GIVEN,
        email_addresses: List[str] | NotGiven = NOT_GIVEN,
        full_names: List[str] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        modified_at: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        order: SortOrder | NotGiven = NOT_GIVEN,
        phone_numbers: List[str] | NotGiven = NOT_GIVEN,
        sort: Literal["created_at"] | NotGiven = NOT_GIVEN,
        user_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        user_status: Literal["active", "archived", "all"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UserListResponse:
        """Retrieves a list of all users associated with the account.

        Optionally, filter by
        user ID to receive specific user information

        Args:
          created_at: Parameter specifying the date in Unix format (in seconds). Only users created
              after this date will be included in the results.

          email_addresses: List of email addresses to filter by (in format test@test.com).

          full_names: List of full names to filter by. Specify the exact first and last name with a
              space between them as shown in the platform (ignore capitalization).

          limit: The maximum number of results to display per page

          modified_at: Parameter specifying the date in in Unix format (in seconds). Only users with
              fields updated after this date will be included in the results.

          offset: The resource offset of the last successfully read resource will be returned as
              the paging.offset JSON property of a paginated response containing more results

          order: An enumeration.

          phone_numbers: List of phone numbers to filter by (in format +<country code><phone number>).

          sort: An enumeration.

          user_ids: List of user IDs for filtering.

          user_status: An enumeration.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/users/v1/users",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "created_at": created_at,
                        "email_addresses": email_addresses,
                        "full_names": full_names,
                        "limit": limit,
                        "modified_at": modified_at,
                        "offset": offset,
                        "order": order,
                        "phone_numbers": phone_numbers,
                        "sort": sort,
                        "user_ids": user_ids,
                        "user_status": user_status,
                    },
                    user_list_params.UserListParams,
                ),
            ),
            cast_to=UserListResponse,
        )

    async def archive(
        self,
        *,
        body: Iterable[int],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UserArchiveResponse:
        """
        Archive individual or multiple users associated with the account by their unique
        userID.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._delete(
            "/users/v1/users",
            body=await async_maybe_transform(body, Iterable[int]),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UserArchiveResponse,
        )

    async def create_note(
        self,
        user_id: int,
        *,
        text: str,
        title: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UserCreateNoteResponse:
        """
        Create new note on the profile of the specified user

        Args:
          user_id: The unique identifier of user to create note for

          text: The text of the user note to be created

          title: The title of the user note to be created

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            f"/users/v1/users/{user_id}/notes",
            body=await async_maybe_transform(
                {
                    "text": text,
                    "title": title,
                },
                user_create_note_params.UserCreateNoteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UserCreateNoteResponse,
        )

    async def update_performance(
        self,
        date: Union[str, date],
        *,
        user_id: int,
        items: Iterable[user_update_performance_params.Item],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UserUpdatePerformanceResponse:
        """Update or add performance data values for a specific user on a given date.

        If a
        value already exists for that date, it will be replaced with the new value. If
        no value exists, the new value will be added.

        Args:
          user_id: The ID of the user whose data is being accessed or modified

          date: The date to which the value(s) will be added, specified in ISO 8601 format
              (e.g., 2025-01-25)

          items: List of performance data values to update

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not date:
            raise ValueError(f"Expected a non-empty value for `date` but received {date!r}")
        return await self._put(
            f"/users/v1/users/{user_id}/performance/{date}",
            body=await async_maybe_transform(
                {"items": items}, user_update_performance_params.UserUpdatePerformanceParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UserUpdatePerformanceResponse,
        )

    async def upload_payslip(
        self,
        user_id: int,
        *,
        end_date: str,
        file_id: str,
        start_date: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIResponseBase:
        """Upload a payslip for a user for a specified period.

        The payslip attachment must
        be uploaded first via the attachments endpoint.

        Args:
          user_id: The unique identifier of the user

          end_date: The end date for the payslip in ISO 8601 format (YYYY-MM-DD)

          file_id: The unique identifier of the payslip attachment

          start_date: The start date for the payslip in ISO 8601 format (YYYY-MM-DD)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            f"/users/v1/users/{user_id}/payslips",
            body=await async_maybe_transform(
                {
                    "end_date": end_date,
                    "file_id": file_id,
                    "start_date": start_date,
                },
                user_upload_payslip_params.UserUploadPayslipParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIResponseBase,
        )


class UsersResourceWithRawResponse:
    def __init__(self, users: UsersResource) -> None:
        self._users = users

        self.create = to_raw_response_wrapper(
            users.create,
        )
        self.update = to_raw_response_wrapper(
            users.update,
        )
        self.list = to_raw_response_wrapper(
            users.list,
        )
        self.archive = to_raw_response_wrapper(
            users.archive,
        )
        self.create_note = to_raw_response_wrapper(
            users.create_note,
        )
        self.update_performance = to_raw_response_wrapper(
            users.update_performance,
        )
        self.upload_payslip = to_raw_response_wrapper(
            users.upload_payslip,
        )


class AsyncUsersResourceWithRawResponse:
    def __init__(self, users: AsyncUsersResource) -> None:
        self._users = users

        self.create = async_to_raw_response_wrapper(
            users.create,
        )
        self.update = async_to_raw_response_wrapper(
            users.update,
        )
        self.list = async_to_raw_response_wrapper(
            users.list,
        )
        self.archive = async_to_raw_response_wrapper(
            users.archive,
        )
        self.create_note = async_to_raw_response_wrapper(
            users.create_note,
        )
        self.update_performance = async_to_raw_response_wrapper(
            users.update_performance,
        )
        self.upload_payslip = async_to_raw_response_wrapper(
            users.upload_payslip,
        )


class UsersResourceWithStreamingResponse:
    def __init__(self, users: UsersResource) -> None:
        self._users = users

        self.create = to_streamed_response_wrapper(
            users.create,
        )
        self.update = to_streamed_response_wrapper(
            users.update,
        )
        self.list = to_streamed_response_wrapper(
            users.list,
        )
        self.archive = to_streamed_response_wrapper(
            users.archive,
        )
        self.create_note = to_streamed_response_wrapper(
            users.create_note,
        )
        self.update_performance = to_streamed_response_wrapper(
            users.update_performance,
        )
        self.upload_payslip = to_streamed_response_wrapper(
            users.upload_payslip,
        )


class AsyncUsersResourceWithStreamingResponse:
    def __init__(self, users: AsyncUsersResource) -> None:
        self._users = users

        self.create = async_to_streamed_response_wrapper(
            users.create,
        )
        self.update = async_to_streamed_response_wrapper(
            users.update,
        )
        self.list = async_to_streamed_response_wrapper(
            users.list,
        )
        self.archive = async_to_streamed_response_wrapper(
            users.archive,
        )
        self.create_note = async_to_streamed_response_wrapper(
            users.create_note,
        )
        self.update_performance = async_to_streamed_response_wrapper(
            users.update_performance,
        )
        self.upload_payslip = async_to_streamed_response_wrapper(
            users.upload_payslip,
        )
