# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

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
from .form_submissions import (
    FormSubmissionsResource,
    AsyncFormSubmissionsResource,
    FormSubmissionsResourceWithRawResponse,
    AsyncFormSubmissionsResourceWithRawResponse,
    FormSubmissionsResourceWithStreamingResponse,
    AsyncFormSubmissionsResourceWithStreamingResponse,
)
from .....types.forms.v1 import form_list_params
from .....types.forms.v1.form_list_response import FormListResponse
from .....types.forms.v1.form_retrieve_response import FormRetrieveResponse

__all__ = ["FormsResource", "AsyncFormsResource"]


class FormsResource(SyncAPIResource):
    @cached_property
    def form_submissions(self) -> FormSubmissionsResource:
        return FormSubmissionsResource(self._client)

    @cached_property
    def with_raw_response(self) -> FormsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return FormsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FormsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return FormsResourceWithStreamingResponse(self)

    def retrieve(
        self,
        form_id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FormRetrieveResponse:
        """
        Retrieve single form information by its unique ID

        Args:
          form_id: Form id to return

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            f"/forms/v1/forms/{form_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FormRetrieveResponse,
        )

    def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FormListResponse:
        """
        Retrieve a list of forms associated with the account

        Args:
          limit: The maximum number of results to display per page

          offset: The resource offset of the last successfully read resource will be returned as
              the paging.offset JSON property of a paginated response containing more results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/forms/v1/forms",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                    },
                    form_list_params.FormListParams,
                ),
            ),
            cast_to=FormListResponse,
        )


class AsyncFormsResource(AsyncAPIResource):
    @cached_property
    def form_submissions(self) -> AsyncFormSubmissionsResource:
        return AsyncFormSubmissionsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncFormsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncFormsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFormsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return AsyncFormsResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        form_id: int,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FormRetrieveResponse:
        """
        Retrieve single form information by its unique ID

        Args:
          form_id: Form id to return

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            f"/forms/v1/forms/{form_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=FormRetrieveResponse,
        )

    async def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FormListResponse:
        """
        Retrieve a list of forms associated with the account

        Args:
          limit: The maximum number of results to display per page

          offset: The resource offset of the last successfully read resource will be returned as
              the paging.offset JSON property of a paginated response containing more results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/forms/v1/forms",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                    },
                    form_list_params.FormListParams,
                ),
            ),
            cast_to=FormListResponse,
        )


class FormsResourceWithRawResponse:
    def __init__(self, forms: FormsResource) -> None:
        self._forms = forms

        self.retrieve = to_raw_response_wrapper(
            forms.retrieve,
        )
        self.list = to_raw_response_wrapper(
            forms.list,
        )

    @cached_property
    def form_submissions(self) -> FormSubmissionsResourceWithRawResponse:
        return FormSubmissionsResourceWithRawResponse(self._forms.form_submissions)


class AsyncFormsResourceWithRawResponse:
    def __init__(self, forms: AsyncFormsResource) -> None:
        self._forms = forms

        self.retrieve = async_to_raw_response_wrapper(
            forms.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            forms.list,
        )

    @cached_property
    def form_submissions(self) -> AsyncFormSubmissionsResourceWithRawResponse:
        return AsyncFormSubmissionsResourceWithRawResponse(self._forms.form_submissions)


class FormsResourceWithStreamingResponse:
    def __init__(self, forms: FormsResource) -> None:
        self._forms = forms

        self.retrieve = to_streamed_response_wrapper(
            forms.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            forms.list,
        )

    @cached_property
    def form_submissions(self) -> FormSubmissionsResourceWithStreamingResponse:
        return FormSubmissionsResourceWithStreamingResponse(self._forms.form_submissions)


class AsyncFormsResourceWithStreamingResponse:
    def __init__(self, forms: AsyncFormsResource) -> None:
        self._forms = forms

        self.retrieve = async_to_streamed_response_wrapper(
            forms.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            forms.list,
        )

    @cached_property
    def form_submissions(self) -> AsyncFormSubmissionsResourceWithStreamingResponse:
        return AsyncFormSubmissionsResourceWithStreamingResponse(self._forms.form_submissions)
