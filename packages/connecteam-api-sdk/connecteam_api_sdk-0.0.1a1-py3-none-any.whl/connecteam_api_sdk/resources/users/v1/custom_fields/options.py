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
from .....types.users.v1.custom_fields import option_list_params, option_create_params, option_update_params
from .....types.users.v1.custom_fields.api_response_base import APIResponseBase
from .....types.users.v1.custom_fields.option_list_response import OptionListResponse
from .....types.users.v1.custom_fields.api_response_dropdown_custom_field_option import (
    APIResponseDropdownCustomFieldOption,
)

__all__ = ["OptionsResource", "AsyncOptionsResource"]


class OptionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> OptionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return OptionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> OptionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return OptionsResourceWithStreamingResponse(self)

    def create(
        self,
        custom_field_id: int,
        *,
        value: str,
        is_disabled: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIResponseDropdownCustomFieldOption:
        """
        Add new option for a specified custom field.The option will be added to the
        existing ones and will not overwrite them.Currently supports dropdown custom
        fields options.

        Args:
          custom_field_id: The unique identifier of the custom field

          value: The value to be added as the option

          is_disabled: Indicates if this option is disabled

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            f"/users/v1/custom-fields/{custom_field_id}/options",
            body=maybe_transform(
                {
                    "value": value,
                    "is_disabled": is_disabled,
                },
                option_create_params.OptionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIResponseDropdownCustomFieldOption,
        )

    def update(
        self,
        option_id: int,
        *,
        custom_field_id: int,
        is_disabled: bool | NotGiven = NOT_GIVEN,
        value: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIResponseDropdownCustomFieldOption:
        """
        Update the value for an option under a specified custom field

        Args:
          custom_field_id: The unique identifier of the custom field

          option_id: The unique identifier of the option to update

          is_disabled: Indicates if this option is disabled

          value: The value to be added as the option

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._put(
            f"/users/v1/custom-fields/{custom_field_id}/options/{option_id}",
            body=maybe_transform(
                {
                    "is_disabled": is_disabled,
                    "value": value,
                },
                option_update_params.OptionUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIResponseDropdownCustomFieldOption,
        )

    def list(
        self,
        custom_field_id: int,
        *,
        is_deleted: bool | NotGiven = NOT_GIVEN,
        is_disabled: bool | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OptionListResponse:
        """
        Retrieve a list of all dropdown value options under a specified custom field

        Args:
          custom_field_id: The unique identifier of the custom field

          is_deleted: Parameter specifying the if to filter only for deleted options.

          is_disabled: Parameter specifying the if to filter only for disabled options.

          limit: The maximum number of results to display per page

          offset: The resource offset of the last successfully read resource will be returned as
              the paging.offset JSON property of a paginated response containing more results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            f"/users/v1/custom-fields/{custom_field_id}/options",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "is_deleted": is_deleted,
                        "is_disabled": is_disabled,
                        "limit": limit,
                        "offset": offset,
                    },
                    option_list_params.OptionListParams,
                ),
            ),
            cast_to=OptionListResponse,
        )

    def delete(
        self,
        option_id: int,
        *,
        custom_field_id: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIResponseBase:
        """
        Delete the value for an option under a specified custom field

        Args:
          custom_field_id: The unique identifier of the custom field

          option_id: The unique identifier of the option to delete

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._delete(
            f"/users/v1/custom-fields/{custom_field_id}/options/{option_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIResponseBase,
        )


class AsyncOptionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncOptionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncOptionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncOptionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return AsyncOptionsResourceWithStreamingResponse(self)

    async def create(
        self,
        custom_field_id: int,
        *,
        value: str,
        is_disabled: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIResponseDropdownCustomFieldOption:
        """
        Add new option for a specified custom field.The option will be added to the
        existing ones and will not overwrite them.Currently supports dropdown custom
        fields options.

        Args:
          custom_field_id: The unique identifier of the custom field

          value: The value to be added as the option

          is_disabled: Indicates if this option is disabled

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            f"/users/v1/custom-fields/{custom_field_id}/options",
            body=await async_maybe_transform(
                {
                    "value": value,
                    "is_disabled": is_disabled,
                },
                option_create_params.OptionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIResponseDropdownCustomFieldOption,
        )

    async def update(
        self,
        option_id: int,
        *,
        custom_field_id: int,
        is_disabled: bool | NotGiven = NOT_GIVEN,
        value: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIResponseDropdownCustomFieldOption:
        """
        Update the value for an option under a specified custom field

        Args:
          custom_field_id: The unique identifier of the custom field

          option_id: The unique identifier of the option to update

          is_disabled: Indicates if this option is disabled

          value: The value to be added as the option

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._put(
            f"/users/v1/custom-fields/{custom_field_id}/options/{option_id}",
            body=await async_maybe_transform(
                {
                    "is_disabled": is_disabled,
                    "value": value,
                },
                option_update_params.OptionUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIResponseDropdownCustomFieldOption,
        )

    async def list(
        self,
        custom_field_id: int,
        *,
        is_deleted: bool | NotGiven = NOT_GIVEN,
        is_disabled: bool | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> OptionListResponse:
        """
        Retrieve a list of all dropdown value options under a specified custom field

        Args:
          custom_field_id: The unique identifier of the custom field

          is_deleted: Parameter specifying the if to filter only for deleted options.

          is_disabled: Parameter specifying the if to filter only for disabled options.

          limit: The maximum number of results to display per page

          offset: The resource offset of the last successfully read resource will be returned as
              the paging.offset JSON property of a paginated response containing more results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            f"/users/v1/custom-fields/{custom_field_id}/options",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "is_deleted": is_deleted,
                        "is_disabled": is_disabled,
                        "limit": limit,
                        "offset": offset,
                    },
                    option_list_params.OptionListParams,
                ),
            ),
            cast_to=OptionListResponse,
        )

    async def delete(
        self,
        option_id: int,
        *,
        custom_field_id: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIResponseBase:
        """
        Delete the value for an option under a specified custom field

        Args:
          custom_field_id: The unique identifier of the custom field

          option_id: The unique identifier of the option to delete

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._delete(
            f"/users/v1/custom-fields/{custom_field_id}/options/{option_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIResponseBase,
        )


class OptionsResourceWithRawResponse:
    def __init__(self, options: OptionsResource) -> None:
        self._options = options

        self.create = to_raw_response_wrapper(
            options.create,
        )
        self.update = to_raw_response_wrapper(
            options.update,
        )
        self.list = to_raw_response_wrapper(
            options.list,
        )
        self.delete = to_raw_response_wrapper(
            options.delete,
        )


class AsyncOptionsResourceWithRawResponse:
    def __init__(self, options: AsyncOptionsResource) -> None:
        self._options = options

        self.create = async_to_raw_response_wrapper(
            options.create,
        )
        self.update = async_to_raw_response_wrapper(
            options.update,
        )
        self.list = async_to_raw_response_wrapper(
            options.list,
        )
        self.delete = async_to_raw_response_wrapper(
            options.delete,
        )


class OptionsResourceWithStreamingResponse:
    def __init__(self, options: OptionsResource) -> None:
        self._options = options

        self.create = to_streamed_response_wrapper(
            options.create,
        )
        self.update = to_streamed_response_wrapper(
            options.update,
        )
        self.list = to_streamed_response_wrapper(
            options.list,
        )
        self.delete = to_streamed_response_wrapper(
            options.delete,
        )


class AsyncOptionsResourceWithStreamingResponse:
    def __init__(self, options: AsyncOptionsResource) -> None:
        self._options = options

        self.create = async_to_streamed_response_wrapper(
            options.create,
        )
        self.update = async_to_streamed_response_wrapper(
            options.update,
        )
        self.list = async_to_streamed_response_wrapper(
            options.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            options.delete,
        )
