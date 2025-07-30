# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from .v1 import (
    V1Resource,
    AsyncV1Resource,
    V1ResourceWithRawResponse,
    AsyncV1ResourceWithRawResponse,
    V1ResourceWithStreamingResponse,
    AsyncV1ResourceWithStreamingResponse,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource

__all__ = ["PublishersResource", "AsyncPublishersResource"]


class PublishersResource(SyncAPIResource):
    @cached_property
    def v1(self) -> V1Resource:
        return V1Resource(self._client)

    @cached_property
    def with_raw_response(self) -> PublishersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return PublishersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PublishersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return PublishersResourceWithStreamingResponse(self)


class AsyncPublishersResource(AsyncAPIResource):
    @cached_property
    def v1(self) -> AsyncV1Resource:
        return AsyncV1Resource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncPublishersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPublishersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPublishersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return AsyncPublishersResourceWithStreamingResponse(self)


class PublishersResourceWithRawResponse:
    def __init__(self, publishers: PublishersResource) -> None:
        self._publishers = publishers

    @cached_property
    def v1(self) -> V1ResourceWithRawResponse:
        return V1ResourceWithRawResponse(self._publishers.v1)


class AsyncPublishersResourceWithRawResponse:
    def __init__(self, publishers: AsyncPublishersResource) -> None:
        self._publishers = publishers

    @cached_property
    def v1(self) -> AsyncV1ResourceWithRawResponse:
        return AsyncV1ResourceWithRawResponse(self._publishers.v1)


class PublishersResourceWithStreamingResponse:
    def __init__(self, publishers: PublishersResource) -> None:
        self._publishers = publishers

    @cached_property
    def v1(self) -> V1ResourceWithStreamingResponse:
        return V1ResourceWithStreamingResponse(self._publishers.v1)


class AsyncPublishersResourceWithStreamingResponse:
    def __init__(self, publishers: AsyncPublishersResource) -> None:
        self._publishers = publishers

    @cached_property
    def v1(self) -> AsyncV1ResourceWithStreamingResponse:
        return AsyncV1ResourceWithStreamingResponse(self._publishers.v1)
