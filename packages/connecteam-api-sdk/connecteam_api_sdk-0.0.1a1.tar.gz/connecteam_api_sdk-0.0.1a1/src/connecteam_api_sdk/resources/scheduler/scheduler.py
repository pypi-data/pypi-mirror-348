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

__all__ = ["SchedulerResource", "AsyncSchedulerResource"]


class SchedulerResource(SyncAPIResource):
    @cached_property
    def v1(self) -> V1Resource:
        return V1Resource(self._client)

    @cached_property
    def with_raw_response(self) -> SchedulerResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return SchedulerResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SchedulerResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return SchedulerResourceWithStreamingResponse(self)


class AsyncSchedulerResource(AsyncAPIResource):
    @cached_property
    def v1(self) -> AsyncV1Resource:
        return AsyncV1Resource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncSchedulerResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSchedulerResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSchedulerResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return AsyncSchedulerResourceWithStreamingResponse(self)


class SchedulerResourceWithRawResponse:
    def __init__(self, scheduler: SchedulerResource) -> None:
        self._scheduler = scheduler

    @cached_property
    def v1(self) -> V1ResourceWithRawResponse:
        return V1ResourceWithRawResponse(self._scheduler.v1)


class AsyncSchedulerResourceWithRawResponse:
    def __init__(self, scheduler: AsyncSchedulerResource) -> None:
        self._scheduler = scheduler

    @cached_property
    def v1(self) -> AsyncV1ResourceWithRawResponse:
        return AsyncV1ResourceWithRawResponse(self._scheduler.v1)


class SchedulerResourceWithStreamingResponse:
    def __init__(self, scheduler: SchedulerResource) -> None:
        self._scheduler = scheduler

    @cached_property
    def v1(self) -> V1ResourceWithStreamingResponse:
        return V1ResourceWithStreamingResponse(self._scheduler.v1)


class AsyncSchedulerResourceWithStreamingResponse:
    def __init__(self, scheduler: AsyncSchedulerResource) -> None:
        self._scheduler = scheduler

    @cached_property
    def v1(self) -> AsyncV1ResourceWithStreamingResponse:
        return AsyncV1ResourceWithStreamingResponse(self._scheduler.v1)
