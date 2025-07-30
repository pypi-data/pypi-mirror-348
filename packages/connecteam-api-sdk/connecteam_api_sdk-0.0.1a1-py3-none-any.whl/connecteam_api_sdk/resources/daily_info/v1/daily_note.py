# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

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
from ....types.daily_info.v1 import daily_note_update_params
from ....types.daily_info.v1.daily_note_response import DailyNoteResponse
from ....types.daily_info.v1.daily_note_delete_response import DailyNoteDeleteResponse

__all__ = ["DailyNoteResource", "AsyncDailyNoteResource"]


class DailyNoteResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DailyNoteResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return DailyNoteResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DailyNoteResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return DailyNoteResourceWithStreamingResponse(self)

    def retrieve(
        self,
        note_id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DailyNoteResponse:
        """
        Get a single note by its unique identifier

        Args:
          note_id: The unique identifier of the note

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            f"/daily-info/v1/daily-note/{note_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DailyNoteResponse,
        )

    def update(
        self,
        note_id: int,
        *,
        qualified_group_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        qualified_user_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        title: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DailyNoteResponse:
        """
        Update a single note by its unique identifier

        Args:
          note_id: The unique identifier of the note

          qualified_group_ids: The groups qualified to see the note

          qualified_user_ids: The users qualified to see the note

          title: The title of the note

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._put(
            f"/daily-info/v1/daily-note/{note_id}",
            body=maybe_transform(
                {
                    "qualified_group_ids": qualified_group_ids,
                    "qualified_user_ids": qualified_user_ids,
                    "title": title,
                },
                daily_note_update_params.DailyNoteUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DailyNoteResponse,
        )

    def delete(
        self,
        note_id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DailyNoteDeleteResponse:
        """
        Delete a single note by its unique identifier

        Args:
          note_id: The unique identifier of the note

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._delete(
            f"/daily-info/v1/daily-note/{note_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DailyNoteDeleteResponse,
        )


class AsyncDailyNoteResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDailyNoteResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDailyNoteResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDailyNoteResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return AsyncDailyNoteResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        note_id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DailyNoteResponse:
        """
        Get a single note by its unique identifier

        Args:
          note_id: The unique identifier of the note

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            f"/daily-info/v1/daily-note/{note_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DailyNoteResponse,
        )

    async def update(
        self,
        note_id: int,
        *,
        qualified_group_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        qualified_user_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        title: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DailyNoteResponse:
        """
        Update a single note by its unique identifier

        Args:
          note_id: The unique identifier of the note

          qualified_group_ids: The groups qualified to see the note

          qualified_user_ids: The users qualified to see the note

          title: The title of the note

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._put(
            f"/daily-info/v1/daily-note/{note_id}",
            body=await async_maybe_transform(
                {
                    "qualified_group_ids": qualified_group_ids,
                    "qualified_user_ids": qualified_user_ids,
                    "title": title,
                },
                daily_note_update_params.DailyNoteUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DailyNoteResponse,
        )

    async def delete(
        self,
        note_id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DailyNoteDeleteResponse:
        """
        Delete a single note by its unique identifier

        Args:
          note_id: The unique identifier of the note

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._delete(
            f"/daily-info/v1/daily-note/{note_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DailyNoteDeleteResponse,
        )


class DailyNoteResourceWithRawResponse:
    def __init__(self, daily_note: DailyNoteResource) -> None:
        self._daily_note = daily_note

        self.retrieve = to_raw_response_wrapper(
            daily_note.retrieve,
        )
        self.update = to_raw_response_wrapper(
            daily_note.update,
        )
        self.delete = to_raw_response_wrapper(
            daily_note.delete,
        )


class AsyncDailyNoteResourceWithRawResponse:
    def __init__(self, daily_note: AsyncDailyNoteResource) -> None:
        self._daily_note = daily_note

        self.retrieve = async_to_raw_response_wrapper(
            daily_note.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            daily_note.update,
        )
        self.delete = async_to_raw_response_wrapper(
            daily_note.delete,
        )


class DailyNoteResourceWithStreamingResponse:
    def __init__(self, daily_note: DailyNoteResource) -> None:
        self._daily_note = daily_note

        self.retrieve = to_streamed_response_wrapper(
            daily_note.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            daily_note.update,
        )
        self.delete = to_streamed_response_wrapper(
            daily_note.delete,
        )


class AsyncDailyNoteResourceWithStreamingResponse:
    def __init__(self, daily_note: AsyncDailyNoteResource) -> None:
        self._daily_note = daily_note

        self.retrieve = async_to_streamed_response_wrapper(
            daily_note.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            daily_note.update,
        )
        self.delete = async_to_streamed_response_wrapper(
            daily_note.delete,
        )
