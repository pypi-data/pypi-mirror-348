# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

import httpx

from ....._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ....._utils import maybe_transform, async_maybe_transform
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....._base_client import make_request_options
from .....types.forms.v1.forms import form_submission_list_params, form_submission_update_params
from .....types.forms.v1.forms.form_submission_list_response import FormSubmissionListResponse
from .....types.forms.v1.forms.form_submission_update_response import FormSubmissionUpdateResponse
from .....types.forms.v1.forms.form_submission_retrieve_response import FormSubmissionRetrieveResponse

__all__ = ["FormSubmissionsResource", "AsyncFormSubmissionsResource"]


class FormSubmissionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> FormSubmissionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return FormSubmissionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FormSubmissionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return FormSubmissionsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        form_submission_id: str,
        *,
        form_id: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FormSubmissionRetrieveResponse:
        """
        Retrieve a single form submission by form submission ID

        Args:
          form_id: Form Id

          form_submission_id: Filter by Form submission id

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not form_submission_id:
            raise ValueError(f"Expected a non-empty value for `form_submission_id` but received {form_submission_id!r}")
        return self._get(
            f"/forms/v1/forms/{form_id}/form-submissions/{form_submission_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FormSubmissionRetrieveResponse,
        )

    def update(
        self,
        form_submission_id: str,
        *,
        form_id: int,
        manager_fields: Iterable[form_submission_update_params.ManagerField],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FormSubmissionUpdateResponse:
        """Update a single form submission by form submission ID.

        Currently, updates are
        only supported for manager fields.

        Args:
          form_id: Form Id

          form_submission_id: Filter by Form submission id

          manager_fields: The manager fields to update

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not form_submission_id:
            raise ValueError(f"Expected a non-empty value for `form_submission_id` but received {form_submission_id!r}")
        return self._put(
            f"/forms/v1/forms/{form_id}/form-submissions/{form_submission_id}",
            body=maybe_transform(
                {"manager_fields": manager_fields}, form_submission_update_params.FormSubmissionUpdateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FormSubmissionUpdateResponse,
        )

    def list(
        self,
        form_id: int,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        submitting_end_time: int | NotGiven = NOT_GIVEN,
        submitting_start_timestamp: int | NotGiven = NOT_GIVEN,
        user_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FormSubmissionListResponse:
        """
        Retrieve a list of form submissions by form ID

        Args:
          form_id: Form Id

          limit: The maximum number of results to display per page

          offset: The resource offset of the last successfully read resource will be returned as
              the paging.offset JSON property of a paginated response containing more results

          submitting_end_time: Filter form submissions that were submitted until this timestamp

          submitting_start_timestamp: Filter form submissions that were submitted from this timestamp

          user_ids: Filter by submitting user ids

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            f"/forms/v1/forms/{form_id}/form-submissions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                        "submitting_end_time": submitting_end_time,
                        "submitting_start_timestamp": submitting_start_timestamp,
                        "user_ids": user_ids,
                    },
                    form_submission_list_params.FormSubmissionListParams,
                ),
            ),
            cast_to=FormSubmissionListResponse,
        )


class AsyncFormSubmissionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncFormSubmissionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncFormSubmissionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFormSubmissionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return AsyncFormSubmissionsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        form_submission_id: str,
        *,
        form_id: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FormSubmissionRetrieveResponse:
        """
        Retrieve a single form submission by form submission ID

        Args:
          form_id: Form Id

          form_submission_id: Filter by Form submission id

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not form_submission_id:
            raise ValueError(f"Expected a non-empty value for `form_submission_id` but received {form_submission_id!r}")
        return await self._get(
            f"/forms/v1/forms/{form_id}/form-submissions/{form_submission_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FormSubmissionRetrieveResponse,
        )

    async def update(
        self,
        form_submission_id: str,
        *,
        form_id: int,
        manager_fields: Iterable[form_submission_update_params.ManagerField],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FormSubmissionUpdateResponse:
        """Update a single form submission by form submission ID.

        Currently, updates are
        only supported for manager fields.

        Args:
          form_id: Form Id

          form_submission_id: Filter by Form submission id

          manager_fields: The manager fields to update

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not form_submission_id:
            raise ValueError(f"Expected a non-empty value for `form_submission_id` but received {form_submission_id!r}")
        return await self._put(
            f"/forms/v1/forms/{form_id}/form-submissions/{form_submission_id}",
            body=await async_maybe_transform(
                {"manager_fields": manager_fields}, form_submission_update_params.FormSubmissionUpdateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FormSubmissionUpdateResponse,
        )

    async def list(
        self,
        form_id: int,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        submitting_end_time: int | NotGiven = NOT_GIVEN,
        submitting_start_timestamp: int | NotGiven = NOT_GIVEN,
        user_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FormSubmissionListResponse:
        """
        Retrieve a list of form submissions by form ID

        Args:
          form_id: Form Id

          limit: The maximum number of results to display per page

          offset: The resource offset of the last successfully read resource will be returned as
              the paging.offset JSON property of a paginated response containing more results

          submitting_end_time: Filter form submissions that were submitted until this timestamp

          submitting_start_timestamp: Filter form submissions that were submitted from this timestamp

          user_ids: Filter by submitting user ids

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            f"/forms/v1/forms/{form_id}/form-submissions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                        "submitting_end_time": submitting_end_time,
                        "submitting_start_timestamp": submitting_start_timestamp,
                        "user_ids": user_ids,
                    },
                    form_submission_list_params.FormSubmissionListParams,
                ),
            ),
            cast_to=FormSubmissionListResponse,
        )


class FormSubmissionsResourceWithRawResponse:
    def __init__(self, form_submissions: FormSubmissionsResource) -> None:
        self._form_submissions = form_submissions

        self.retrieve = to_raw_response_wrapper(
            form_submissions.retrieve,
        )
        self.update = to_raw_response_wrapper(
            form_submissions.update,
        )
        self.list = to_raw_response_wrapper(
            form_submissions.list,
        )


class AsyncFormSubmissionsResourceWithRawResponse:
    def __init__(self, form_submissions: AsyncFormSubmissionsResource) -> None:
        self._form_submissions = form_submissions

        self.retrieve = async_to_raw_response_wrapper(
            form_submissions.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            form_submissions.update,
        )
        self.list = async_to_raw_response_wrapper(
            form_submissions.list,
        )


class FormSubmissionsResourceWithStreamingResponse:
    def __init__(self, form_submissions: FormSubmissionsResource) -> None:
        self._form_submissions = form_submissions

        self.retrieve = to_streamed_response_wrapper(
            form_submissions.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            form_submissions.update,
        )
        self.list = to_streamed_response_wrapper(
            form_submissions.list,
        )


class AsyncFormSubmissionsResourceWithStreamingResponse:
    def __init__(self, form_submissions: AsyncFormSubmissionsResource) -> None:
        self._form_submissions = form_submissions

        self.retrieve = async_to_streamed_response_wrapper(
            form_submissions.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            form_submissions.update,
        )
        self.list = async_to_streamed_response_wrapper(
            form_submissions.list,
        )
