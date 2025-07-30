# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import maybe_transform, async_maybe_transform
from ...._compat import cached_property
from .daily_note import (
    DailyNoteResource,
    AsyncDailyNoteResource,
    DailyNoteResourceWithRawResponse,
    AsyncDailyNoteResourceWithRawResponse,
    DailyNoteResourceWithStreamingResponse,
    AsyncDailyNoteResourceWithStreamingResponse,
)
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.daily_info import v1_create_daily_note_params
from ....types.daily_info.v1.daily_note_response import DailyNoteResponse

__all__ = ["V1Resource", "AsyncV1Resource"]


class V1Resource(SyncAPIResource):
    @cached_property
    def daily_note(self) -> DailyNoteResource:
        return DailyNoteResource(self._client)

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

    def create_daily_note(
        self,
        *,
        date: str,
        instance_id: int,
        title: str,
        qualified_group_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        qualified_user_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DailyNoteResponse:
        """
        Create a note under a specified scheduler for a specific date

        Args:
          date: The date for the note in ISO 8601 format (e.g. YYYY-MM-DD)

          instance_id: The unique identifier of the scheduler

          title: The title of the note

          qualified_group_ids: The groups qualified to see the note

          qualified_user_ids: The users qualified to see the note

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/daily-info/v1/daily-notes",
            body=maybe_transform(
                {
                    "date": date,
                    "instance_id": instance_id,
                    "title": title,
                    "qualified_group_ids": qualified_group_ids,
                    "qualified_user_ids": qualified_user_ids,
                },
                v1_create_daily_note_params.V1CreateDailyNoteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DailyNoteResponse,
        )


class AsyncV1Resource(AsyncAPIResource):
    @cached_property
    def daily_note(self) -> AsyncDailyNoteResource:
        return AsyncDailyNoteResource(self._client)

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

    async def create_daily_note(
        self,
        *,
        date: str,
        instance_id: int,
        title: str,
        qualified_group_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        qualified_user_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> DailyNoteResponse:
        """
        Create a note under a specified scheduler for a specific date

        Args:
          date: The date for the note in ISO 8601 format (e.g. YYYY-MM-DD)

          instance_id: The unique identifier of the scheduler

          title: The title of the note

          qualified_group_ids: The groups qualified to see the note

          qualified_user_ids: The users qualified to see the note

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/daily-info/v1/daily-notes",
            body=await async_maybe_transform(
                {
                    "date": date,
                    "instance_id": instance_id,
                    "title": title,
                    "qualified_group_ids": qualified_group_ids,
                    "qualified_user_ids": qualified_user_ids,
                },
                v1_create_daily_note_params.V1CreateDailyNoteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DailyNoteResponse,
        )


class V1ResourceWithRawResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

        self.create_daily_note = to_raw_response_wrapper(
            v1.create_daily_note,
        )

    @cached_property
    def daily_note(self) -> DailyNoteResourceWithRawResponse:
        return DailyNoteResourceWithRawResponse(self._v1.daily_note)


class AsyncV1ResourceWithRawResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

        self.create_daily_note = async_to_raw_response_wrapper(
            v1.create_daily_note,
        )

    @cached_property
    def daily_note(self) -> AsyncDailyNoteResourceWithRawResponse:
        return AsyncDailyNoteResourceWithRawResponse(self._v1.daily_note)


class V1ResourceWithStreamingResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

        self.create_daily_note = to_streamed_response_wrapper(
            v1.create_daily_note,
        )

    @cached_property
    def daily_note(self) -> DailyNoteResourceWithStreamingResponse:
        return DailyNoteResourceWithStreamingResponse(self._v1.daily_note)


class AsyncV1ResourceWithStreamingResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

        self.create_daily_note = async_to_streamed_response_wrapper(
            v1.create_daily_note,
        )

    @cached_property
    def daily_note(self) -> AsyncDailyNoteResourceWithStreamingResponse:
        return AsyncDailyNoteResourceWithStreamingResponse(self._v1.daily_note)
