# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

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
from ....types.attachments.v1 import file_generate_upload_url_params
from ....types.attachments.v1.file_retrieve_response import FileRetrieveResponse
from ....types.attachments.v1.file_complete_upload_response import FileCompleteUploadResponse
from ....types.attachments.v1.file_generate_upload_url_response import FileGenerateUploadURLResponse

__all__ = ["FilesResource", "AsyncFilesResource"]


class FilesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> FilesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return FilesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FilesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return FilesResourceWithStreamingResponse(self)

    def retrieve(
        self,
        file_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FileRetrieveResponse:
        """
        Retrieve detailed information about a previously uploaded attachment identified
        by the fileId. The response includes its metadata, and the status of the upload
        process.

        Args:
          file_id: The unique identifier for the uploaded filetype

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not file_id:
            raise ValueError(f"Expected a non-empty value for `file_id` but received {file_id!r}")
        return self._get(
            f"/attachments/v1/files/{file_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FileRetrieveResponse,
        )

    def complete_upload(
        self,
        file_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FileCompleteUploadResponse:
        """Finalizes the upload process for the attachment identified by the fileId.

        It
        confirms and registers the uploaded file, ensuring it is properly associated
        with the relevant feature.

        Args:
          file_id: The unique identifier for the uploaded filetype

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not file_id:
            raise ValueError(f"Expected a non-empty value for `file_id` but received {file_id!r}")
        return self._put(
            f"/attachments/v1/files/complete-upload/{file_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FileCompleteUploadResponse,
        )

    def generate_upload_url(
        self,
        *,
        feature_type: Literal["chat", "shiftscheduler", "users"],
        file_name: str,
        file_type_hint: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FileGenerateUploadURLResponse:
        """
        Generates a pre-signed URL that can be used to securely upload an attachment to
        the cloud. The pre-signed URL ensures temporary access for the upload (300
        seconds), and it will be associated with a specific feature within the
        application.

        Args:
          feature_type: An enumeration.

          file_name: The name of the attachment you want to upload

          file_type_hint: The MIME type or format of the attachment (e.g. image/jpeg, application/pdf)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/attachments/v1/files/generate-upload-url",
            body=maybe_transform(
                {
                    "feature_type": feature_type,
                    "file_name": file_name,
                    "file_type_hint": file_type_hint,
                },
                file_generate_upload_url_params.FileGenerateUploadURLParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FileGenerateUploadURLResponse,
        )


class AsyncFilesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncFilesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncFilesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFilesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return AsyncFilesResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        file_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FileRetrieveResponse:
        """
        Retrieve detailed information about a previously uploaded attachment identified
        by the fileId. The response includes its metadata, and the status of the upload
        process.

        Args:
          file_id: The unique identifier for the uploaded filetype

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not file_id:
            raise ValueError(f"Expected a non-empty value for `file_id` but received {file_id!r}")
        return await self._get(
            f"/attachments/v1/files/{file_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FileRetrieveResponse,
        )

    async def complete_upload(
        self,
        file_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FileCompleteUploadResponse:
        """Finalizes the upload process for the attachment identified by the fileId.

        It
        confirms and registers the uploaded file, ensuring it is properly associated
        with the relevant feature.

        Args:
          file_id: The unique identifier for the uploaded filetype

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not file_id:
            raise ValueError(f"Expected a non-empty value for `file_id` but received {file_id!r}")
        return await self._put(
            f"/attachments/v1/files/complete-upload/{file_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FileCompleteUploadResponse,
        )

    async def generate_upload_url(
        self,
        *,
        feature_type: Literal["chat", "shiftscheduler", "users"],
        file_name: str,
        file_type_hint: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FileGenerateUploadURLResponse:
        """
        Generates a pre-signed URL that can be used to securely upload an attachment to
        the cloud. The pre-signed URL ensures temporary access for the upload (300
        seconds), and it will be associated with a specific feature within the
        application.

        Args:
          feature_type: An enumeration.

          file_name: The name of the attachment you want to upload

          file_type_hint: The MIME type or format of the attachment (e.g. image/jpeg, application/pdf)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/attachments/v1/files/generate-upload-url",
            body=await async_maybe_transform(
                {
                    "feature_type": feature_type,
                    "file_name": file_name,
                    "file_type_hint": file_type_hint,
                },
                file_generate_upload_url_params.FileGenerateUploadURLParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FileGenerateUploadURLResponse,
        )


class FilesResourceWithRawResponse:
    def __init__(self, files: FilesResource) -> None:
        self._files = files

        self.retrieve = to_raw_response_wrapper(
            files.retrieve,
        )
        self.complete_upload = to_raw_response_wrapper(
            files.complete_upload,
        )
        self.generate_upload_url = to_raw_response_wrapper(
            files.generate_upload_url,
        )


class AsyncFilesResourceWithRawResponse:
    def __init__(self, files: AsyncFilesResource) -> None:
        self._files = files

        self.retrieve = async_to_raw_response_wrapper(
            files.retrieve,
        )
        self.complete_upload = async_to_raw_response_wrapper(
            files.complete_upload,
        )
        self.generate_upload_url = async_to_raw_response_wrapper(
            files.generate_upload_url,
        )


class FilesResourceWithStreamingResponse:
    def __init__(self, files: FilesResource) -> None:
        self._files = files

        self.retrieve = to_streamed_response_wrapper(
            files.retrieve,
        )
        self.complete_upload = to_streamed_response_wrapper(
            files.complete_upload,
        )
        self.generate_upload_url = to_streamed_response_wrapper(
            files.generate_upload_url,
        )


class AsyncFilesResourceWithStreamingResponse:
    def __init__(self, files: AsyncFilesResource) -> None:
        self._files = files

        self.retrieve = async_to_streamed_response_wrapper(
            files.retrieve,
        )
        self.complete_upload = async_to_streamed_response_wrapper(
            files.complete_upload,
        )
        self.generate_upload_url = async_to_streamed_response_wrapper(
            files.generate_upload_url,
        )
