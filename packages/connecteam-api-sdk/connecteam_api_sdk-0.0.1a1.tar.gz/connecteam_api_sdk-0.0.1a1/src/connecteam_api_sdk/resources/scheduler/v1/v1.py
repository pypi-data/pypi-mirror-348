# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from .schedulers.schedulers import (
    SchedulersResource,
    AsyncSchedulersResource,
    SchedulersResourceWithRawResponse,
    AsyncSchedulersResourceWithRawResponse,
    SchedulersResourceWithStreamingResponse,
    AsyncSchedulersResourceWithStreamingResponse,
)

__all__ = ["V1Resource", "AsyncV1Resource"]


class V1Resource(SyncAPIResource):
    @cached_property
    def schedulers(self) -> SchedulersResource:
        return SchedulersResource(self._client)

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


class AsyncV1Resource(AsyncAPIResource):
    @cached_property
    def schedulers(self) -> AsyncSchedulersResource:
        return AsyncSchedulersResource(self._client)

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


class V1ResourceWithRawResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

    @cached_property
    def schedulers(self) -> SchedulersResourceWithRawResponse:
        return SchedulersResourceWithRawResponse(self._v1.schedulers)


class AsyncV1ResourceWithRawResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

    @cached_property
    def schedulers(self) -> AsyncSchedulersResourceWithRawResponse:
        return AsyncSchedulersResourceWithRawResponse(self._v1.schedulers)


class V1ResourceWithStreamingResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

    @cached_property
    def schedulers(self) -> SchedulersResourceWithStreamingResponse:
        return SchedulersResourceWithStreamingResponse(self._v1.schedulers)


class AsyncV1ResourceWithStreamingResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

    @cached_property
    def schedulers(self) -> AsyncSchedulersResourceWithStreamingResponse:
        return AsyncSchedulersResourceWithStreamingResponse(self._v1.schedulers)
