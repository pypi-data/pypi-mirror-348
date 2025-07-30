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

__all__ = ["DailyInfoResource", "AsyncDailyInfoResource"]


class DailyInfoResource(SyncAPIResource):
    @cached_property
    def v1(self) -> V1Resource:
        return V1Resource(self._client)

    @cached_property
    def with_raw_response(self) -> DailyInfoResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return DailyInfoResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DailyInfoResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return DailyInfoResourceWithStreamingResponse(self)


class AsyncDailyInfoResource(AsyncAPIResource):
    @cached_property
    def v1(self) -> AsyncV1Resource:
        return AsyncV1Resource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncDailyInfoResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDailyInfoResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDailyInfoResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return AsyncDailyInfoResourceWithStreamingResponse(self)


class DailyInfoResourceWithRawResponse:
    def __init__(self, daily_info: DailyInfoResource) -> None:
        self._daily_info = daily_info

    @cached_property
    def v1(self) -> V1ResourceWithRawResponse:
        return V1ResourceWithRawResponse(self._daily_info.v1)


class AsyncDailyInfoResourceWithRawResponse:
    def __init__(self, daily_info: AsyncDailyInfoResource) -> None:
        self._daily_info = daily_info

    @cached_property
    def v1(self) -> AsyncV1ResourceWithRawResponse:
        return AsyncV1ResourceWithRawResponse(self._daily_info.v1)


class DailyInfoResourceWithStreamingResponse:
    def __init__(self, daily_info: DailyInfoResource) -> None:
        self._daily_info = daily_info

    @cached_property
    def v1(self) -> V1ResourceWithStreamingResponse:
        return V1ResourceWithStreamingResponse(self._daily_info.v1)


class AsyncDailyInfoResourceWithStreamingResponse:
    def __init__(self, daily_info: AsyncDailyInfoResource) -> None:
        self._daily_info = daily_info

    @cached_property
    def v1(self) -> AsyncV1ResourceWithStreamingResponse:
        return AsyncV1ResourceWithStreamingResponse(self._daily_info.v1)
