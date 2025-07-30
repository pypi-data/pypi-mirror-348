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

__all__ = ["TimeOffResource", "AsyncTimeOffResource"]


class TimeOffResource(SyncAPIResource):
    @cached_property
    def v1(self) -> V1Resource:
        return V1Resource(self._client)

    @cached_property
    def with_raw_response(self) -> TimeOffResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return TimeOffResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TimeOffResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return TimeOffResourceWithStreamingResponse(self)


class AsyncTimeOffResource(AsyncAPIResource):
    @cached_property
    def v1(self) -> AsyncV1Resource:
        return AsyncV1Resource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncTimeOffResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTimeOffResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTimeOffResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return AsyncTimeOffResourceWithStreamingResponse(self)


class TimeOffResourceWithRawResponse:
    def __init__(self, time_off: TimeOffResource) -> None:
        self._time_off = time_off

    @cached_property
    def v1(self) -> V1ResourceWithRawResponse:
        return V1ResourceWithRawResponse(self._time_off.v1)


class AsyncTimeOffResourceWithRawResponse:
    def __init__(self, time_off: AsyncTimeOffResource) -> None:
        self._time_off = time_off

    @cached_property
    def v1(self) -> AsyncV1ResourceWithRawResponse:
        return AsyncV1ResourceWithRawResponse(self._time_off.v1)


class TimeOffResourceWithStreamingResponse:
    def __init__(self, time_off: TimeOffResource) -> None:
        self._time_off = time_off

    @cached_property
    def v1(self) -> V1ResourceWithStreamingResponse:
        return V1ResourceWithStreamingResponse(self._time_off.v1)


class AsyncTimeOffResourceWithStreamingResponse:
    def __init__(self, time_off: AsyncTimeOffResource) -> None:
        self._time_off = time_off

    @cached_property
    def v1(self) -> AsyncV1ResourceWithStreamingResponse:
        return AsyncV1ResourceWithStreamingResponse(self._time_off.v1)
