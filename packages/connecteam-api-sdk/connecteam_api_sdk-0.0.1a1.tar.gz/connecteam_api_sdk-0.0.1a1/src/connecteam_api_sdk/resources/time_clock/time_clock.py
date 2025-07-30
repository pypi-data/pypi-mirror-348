# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .v1.v1 import (
    V1Resource,
    AsyncV1Resource,
    V1ResourceWithRawResponse,
    AsyncV1ResourceWithRawResponse,
    V1ResourceWithStreamingResponse,
    AsyncV1ResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["TimeClockResource", "AsyncTimeClockResource"]


class TimeClockResource(SyncAPIResource):
    @cached_property
    def v1(self) -> V1Resource:
        return V1Resource(self._client)

    @cached_property
    def with_raw_response(self) -> TimeClockResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return TimeClockResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TimeClockResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return TimeClockResourceWithStreamingResponse(self)


class AsyncTimeClockResource(AsyncAPIResource):
    @cached_property
    def v1(self) -> AsyncV1Resource:
        return AsyncV1Resource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncTimeClockResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTimeClockResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTimeClockResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return AsyncTimeClockResourceWithStreamingResponse(self)


class TimeClockResourceWithRawResponse:
    def __init__(self, time_clock: TimeClockResource) -> None:
        self._time_clock = time_clock

    @cached_property
    def v1(self) -> V1ResourceWithRawResponse:
        return V1ResourceWithRawResponse(self._time_clock.v1)


class AsyncTimeClockResourceWithRawResponse:
    def __init__(self, time_clock: AsyncTimeClockResource) -> None:
        self._time_clock = time_clock

    @cached_property
    def v1(self) -> AsyncV1ResourceWithRawResponse:
        return AsyncV1ResourceWithRawResponse(self._time_clock.v1)


class TimeClockResourceWithStreamingResponse:
    def __init__(self, time_clock: TimeClockResource) -> None:
        self._time_clock = time_clock

    @cached_property
    def v1(self) -> V1ResourceWithStreamingResponse:
        return V1ResourceWithStreamingResponse(self._time_clock.v1)


class AsyncTimeClockResourceWithStreamingResponse:
    def __init__(self, time_clock: AsyncTimeClockResource) -> None:
        self._time_clock = time_clock

    @cached_property
    def v1(self) -> AsyncV1ResourceWithStreamingResponse:
        return AsyncV1ResourceWithStreamingResponse(self._time_clock.v1)
