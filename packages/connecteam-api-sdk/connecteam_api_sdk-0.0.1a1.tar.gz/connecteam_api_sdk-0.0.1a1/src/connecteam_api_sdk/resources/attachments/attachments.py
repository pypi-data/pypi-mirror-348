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

__all__ = ["AttachmentsResource", "AsyncAttachmentsResource"]


class AttachmentsResource(SyncAPIResource):
    @cached_property
    def v1(self) -> V1Resource:
        return V1Resource(self._client)

    @cached_property
    def with_raw_response(self) -> AttachmentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AttachmentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AttachmentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return AttachmentsResourceWithStreamingResponse(self)


class AsyncAttachmentsResource(AsyncAPIResource):
    @cached_property
    def v1(self) -> AsyncV1Resource:
        return AsyncV1Resource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncAttachmentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAttachmentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAttachmentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return AsyncAttachmentsResourceWithStreamingResponse(self)


class AttachmentsResourceWithRawResponse:
    def __init__(self, attachments: AttachmentsResource) -> None:
        self._attachments = attachments

    @cached_property
    def v1(self) -> V1ResourceWithRawResponse:
        return V1ResourceWithRawResponse(self._attachments.v1)


class AsyncAttachmentsResourceWithRawResponse:
    def __init__(self, attachments: AsyncAttachmentsResource) -> None:
        self._attachments = attachments

    @cached_property
    def v1(self) -> AsyncV1ResourceWithRawResponse:
        return AsyncV1ResourceWithRawResponse(self._attachments.v1)


class AttachmentsResourceWithStreamingResponse:
    def __init__(self, attachments: AttachmentsResource) -> None:
        self._attachments = attachments

    @cached_property
    def v1(self) -> V1ResourceWithStreamingResponse:
        return V1ResourceWithStreamingResponse(self._attachments.v1)


class AsyncAttachmentsResourceWithStreamingResponse:
    def __init__(self, attachments: AsyncAttachmentsResource) -> None:
        self._attachments = attachments

    @cached_property
    def v1(self) -> AsyncV1ResourceWithStreamingResponse:
        return AsyncV1ResourceWithStreamingResponse(self._attachments.v1)
