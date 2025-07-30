# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal

import httpx

from .options import (
    OptionsResource,
    AsyncOptionsResource,
    OptionsResourceWithRawResponse,
    AsyncOptionsResourceWithRawResponse,
    OptionsResourceWithStreamingResponse,
    AsyncOptionsResourceWithStreamingResponse,
)
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
from .....types.users.v1 import (
    custom_field_list_params,
    custom_field_create_params,
    custom_field_delete_params,
    custom_field_update_params,
)
from .....types.scheduler.v1.schedulers import SortOrder
from .....types.users.v1.user_custom_fields import UserCustomFields
from .....types.scheduler.v1.schedulers.sort_order import SortOrder
from .....types.users.v1.custom_field_list_response import CustomFieldListResponse
from .....types.users.v1.custom_field_delete_response import CustomFieldDeleteResponse
from .....types.users.v1.api_response_get_custom_fields_settings import APIResponseGetCustomFieldsSettings

__all__ = ["CustomFieldsResource", "AsyncCustomFieldsResource"]


class CustomFieldsResource(SyncAPIResource):
    @cached_property
    def options(self) -> OptionsResource:
        return OptionsResource(self._client)

    @cached_property
    def with_raw_response(self) -> CustomFieldsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return CustomFieldsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CustomFieldsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return CustomFieldsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        custom_fields: Iterable[custom_field_create_params.CustomField],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIResponseGetCustomFieldsSettings:
        """
        Create individual or multiple custom fields associated with the account under a
        specific category.

        Args:
          custom_fields: The custom fields.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/users/v1/custom-fields",
            body=maybe_transform({"custom_fields": custom_fields}, custom_field_create_params.CustomFieldCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIResponseGetCustomFieldsSettings,
        )

    def update(
        self,
        *,
        custom_fields: Iterable[custom_field_update_params.CustomField],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIResponseGetCustomFieldsSettings:
        """
        Update custom fields settings by their unique ID

        Args:
          custom_fields: The custom fields.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._put(
            "/users/v1/custom-fields",
            body=maybe_transform({"custom_fields": custom_fields}, custom_field_update_params.CustomFieldUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIResponseGetCustomFieldsSettings,
        )

    def list(
        self,
        *,
        category_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        custom_field_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        custom_field_names: List[str] | NotGiven = NOT_GIVEN,
        custom_field_types: List[UserCustomFields] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        order: SortOrder | NotGiven = NOT_GIVEN,
        sort: Literal["id", "name", "type"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CustomFieldListResponse:
        """Retrieves all custom fields associated with the account.

        Optionally, filter the
        results by categories, names, types, or custom field IDs.

        Args:
          category_ids: Custom field category ids to filter by

          custom_field_ids: Custom field ids to filter by

          custom_field_names: Custom field names to filter by

          custom_field_types: Custom field types to filter by

          limit: The maximum number of results to display per page

          offset: The resource offset of the last successfully read resource will be returned as
              the paging.offset JSON property of a paginated response containing more results

          order: An enumeration.

          sort: An enumeration.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/users/v1/custom-fields",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "category_ids": category_ids,
                        "custom_field_ids": custom_field_ids,
                        "custom_field_names": custom_field_names,
                        "custom_field_types": custom_field_types,
                        "limit": limit,
                        "offset": offset,
                        "order": order,
                        "sort": sort,
                    },
                    custom_field_list_params.CustomFieldListParams,
                ),
            ),
            cast_to=CustomFieldListResponse,
        )

    def delete(
        self,
        *,
        custom_field_ids: Iterable[int],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CustomFieldDeleteResponse:
        """
        Delete individual or multiple custom fields associated with the account by their
        unique ID.

        Args:
          custom_field_ids: The custom fields IDs to delete

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._delete(
            "/users/v1/custom-fields",
            body=maybe_transform(
                {"custom_field_ids": custom_field_ids}, custom_field_delete_params.CustomFieldDeleteParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CustomFieldDeleteResponse,
        )


class AsyncCustomFieldsResource(AsyncAPIResource):
    @cached_property
    def options(self) -> AsyncOptionsResource:
        return AsyncOptionsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncCustomFieldsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCustomFieldsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCustomFieldsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return AsyncCustomFieldsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        custom_fields: Iterable[custom_field_create_params.CustomField],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIResponseGetCustomFieldsSettings:
        """
        Create individual or multiple custom fields associated with the account under a
        specific category.

        Args:
          custom_fields: The custom fields.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/users/v1/custom-fields",
            body=await async_maybe_transform(
                {"custom_fields": custom_fields}, custom_field_create_params.CustomFieldCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIResponseGetCustomFieldsSettings,
        )

    async def update(
        self,
        *,
        custom_fields: Iterable[custom_field_update_params.CustomField],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIResponseGetCustomFieldsSettings:
        """
        Update custom fields settings by their unique ID

        Args:
          custom_fields: The custom fields.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._put(
            "/users/v1/custom-fields",
            body=await async_maybe_transform(
                {"custom_fields": custom_fields}, custom_field_update_params.CustomFieldUpdateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIResponseGetCustomFieldsSettings,
        )

    async def list(
        self,
        *,
        category_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        custom_field_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        custom_field_names: List[str] | NotGiven = NOT_GIVEN,
        custom_field_types: List[UserCustomFields] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        order: SortOrder | NotGiven = NOT_GIVEN,
        sort: Literal["id", "name", "type"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CustomFieldListResponse:
        """Retrieves all custom fields associated with the account.

        Optionally, filter the
        results by categories, names, types, or custom field IDs.

        Args:
          category_ids: Custom field category ids to filter by

          custom_field_ids: Custom field ids to filter by

          custom_field_names: Custom field names to filter by

          custom_field_types: Custom field types to filter by

          limit: The maximum number of results to display per page

          offset: The resource offset of the last successfully read resource will be returned as
              the paging.offset JSON property of a paginated response containing more results

          order: An enumeration.

          sort: An enumeration.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/users/v1/custom-fields",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "category_ids": category_ids,
                        "custom_field_ids": custom_field_ids,
                        "custom_field_names": custom_field_names,
                        "custom_field_types": custom_field_types,
                        "limit": limit,
                        "offset": offset,
                        "order": order,
                        "sort": sort,
                    },
                    custom_field_list_params.CustomFieldListParams,
                ),
            ),
            cast_to=CustomFieldListResponse,
        )

    async def delete(
        self,
        *,
        custom_field_ids: Iterable[int],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CustomFieldDeleteResponse:
        """
        Delete individual or multiple custom fields associated with the account by their
        unique ID.

        Args:
          custom_field_ids: The custom fields IDs to delete

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._delete(
            "/users/v1/custom-fields",
            body=await async_maybe_transform(
                {"custom_field_ids": custom_field_ids}, custom_field_delete_params.CustomFieldDeleteParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CustomFieldDeleteResponse,
        )


class CustomFieldsResourceWithRawResponse:
    def __init__(self, custom_fields: CustomFieldsResource) -> None:
        self._custom_fields = custom_fields

        self.create = to_raw_response_wrapper(
            custom_fields.create,
        )
        self.update = to_raw_response_wrapper(
            custom_fields.update,
        )
        self.list = to_raw_response_wrapper(
            custom_fields.list,
        )
        self.delete = to_raw_response_wrapper(
            custom_fields.delete,
        )

    @cached_property
    def options(self) -> OptionsResourceWithRawResponse:
        return OptionsResourceWithRawResponse(self._custom_fields.options)


class AsyncCustomFieldsResourceWithRawResponse:
    def __init__(self, custom_fields: AsyncCustomFieldsResource) -> None:
        self._custom_fields = custom_fields

        self.create = async_to_raw_response_wrapper(
            custom_fields.create,
        )
        self.update = async_to_raw_response_wrapper(
            custom_fields.update,
        )
        self.list = async_to_raw_response_wrapper(
            custom_fields.list,
        )
        self.delete = async_to_raw_response_wrapper(
            custom_fields.delete,
        )

    @cached_property
    def options(self) -> AsyncOptionsResourceWithRawResponse:
        return AsyncOptionsResourceWithRawResponse(self._custom_fields.options)


class CustomFieldsResourceWithStreamingResponse:
    def __init__(self, custom_fields: CustomFieldsResource) -> None:
        self._custom_fields = custom_fields

        self.create = to_streamed_response_wrapper(
            custom_fields.create,
        )
        self.update = to_streamed_response_wrapper(
            custom_fields.update,
        )
        self.list = to_streamed_response_wrapper(
            custom_fields.list,
        )
        self.delete = to_streamed_response_wrapper(
            custom_fields.delete,
        )

    @cached_property
    def options(self) -> OptionsResourceWithStreamingResponse:
        return OptionsResourceWithStreamingResponse(self._custom_fields.options)


class AsyncCustomFieldsResourceWithStreamingResponse:
    def __init__(self, custom_fields: AsyncCustomFieldsResource) -> None:
        self._custom_fields = custom_fields

        self.create = async_to_streamed_response_wrapper(
            custom_fields.create,
        )
        self.update = async_to_streamed_response_wrapper(
            custom_fields.update,
        )
        self.list = async_to_streamed_response_wrapper(
            custom_fields.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            custom_fields.delete,
        )

    @cached_property
    def options(self) -> AsyncOptionsResourceWithStreamingResponse:
        return AsyncOptionsResourceWithStreamingResponse(self._custom_fields.options)
