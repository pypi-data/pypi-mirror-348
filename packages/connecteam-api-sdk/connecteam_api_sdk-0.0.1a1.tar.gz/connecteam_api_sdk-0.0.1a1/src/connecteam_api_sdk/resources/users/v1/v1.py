# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal

import httpx

from .users import (
    UsersResource,
    AsyncUsersResource,
    UsersResourceWithRawResponse,
    AsyncUsersResourceWithRawResponse,
    UsersResourceWithStreamingResponse,
    AsyncUsersResourceWithStreamingResponse,
)
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
from ....types.users import (
    v1_promote_admin_params,
    v1_get_smart_groups_params,
    v1_get_performance_indicators_params,
    v1_get_custom_field_categories_params,
)
from ...._base_client import make_request_options
from .custom_fields.custom_fields import (
    CustomFieldsResource,
    AsyncCustomFieldsResource,
    CustomFieldsResourceWithRawResponse,
    AsyncCustomFieldsResourceWithRawResponse,
    CustomFieldsResourceWithStreamingResponse,
    AsyncCustomFieldsResourceWithStreamingResponse,
)
from ....types.scheduler.v1.schedulers import SortOrder
from ....types.scheduler.v1.schedulers.sort_order import SortOrder
from ....types.users.v1_get_smart_groups_response import V1GetSmartGroupsResponse
from ....types.users.v1.custom_fields.api_response_base import APIResponseBase
from ....types.users.v1_get_performance_indicators_response import V1GetPerformanceIndicatorsResponse
from ....types.users.v1_get_custom_field_categories_response import V1GetCustomFieldCategoriesResponse

__all__ = ["V1Resource", "AsyncV1Resource"]


class V1Resource(SyncAPIResource):
    @cached_property
    def users(self) -> UsersResource:
        return UsersResource(self._client)

    @cached_property
    def custom_fields(self) -> CustomFieldsResource:
        return CustomFieldsResource(self._client)

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

    def get_custom_field_categories(
        self,
        *,
        category_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        category_names: List[str] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        order: SortOrder | NotGiven = NOT_GIVEN,
        sort: Literal["id", "name"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> V1GetCustomFieldCategoriesResponse:
        """Retrieves all custom fields categories associated with the account.

        Optionally,
        filter the results by category IDs and/or names.

        Args:
          category_ids: Custom field category ids to filter by

          category_names: Custom field category names to filter by

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
            "/users/v1/custom-field-categories",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "category_ids": category_ids,
                        "category_names": category_names,
                        "limit": limit,
                        "offset": offset,
                        "order": order,
                        "sort": sort,
                    },
                    v1_get_custom_field_categories_params.V1GetCustomFieldCategoriesParams,
                ),
            ),
            cast_to=V1GetCustomFieldCategoriesResponse,
        )

    def get_performance_indicators(
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
    ) -> V1GetPerformanceIndicatorsResponse:
        """
        Retrieve the metric indicators of the performance data associated with account.

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
            "/users/v1/performance-indicators",
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
                    v1_get_performance_indicators_params.V1GetPerformanceIndicatorsParams,
                ),
            ),
            cast_to=V1GetPerformanceIndicatorsResponse,
        )

    def get_smart_groups(
        self,
        *,
        id: int | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> V1GetSmartGroupsResponse:
        """
        Retrieves a list of smart groups associated with the account.

        Args:
          id: The unique identifier of the smart group.

          name: The name of the smart group to filter by.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/users/v1/smart-groups",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "id": id,
                        "name": name,
                    },
                    v1_get_smart_groups_params.V1GetSmartGroupsParams,
                ),
            ),
            cast_to=V1GetSmartGroupsResponse,
        )

    def promote_admin(
        self,
        *,
        email: str,
        title: str,
        user_id: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIResponseBase:
        """Promote an existing user to an admin.

        An invitation link will be sent to the
        specified email address of the user

        Args:
          email: The email address of the user to be promoted. An invitation link will be sent to
              the specified email. Once the user acknowledges the email, the user will become
              an admin of the account.

          title: The title of the user to be promoted

          user_id: The unique identifier of the user to be promoted to admin

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/users/v1/admins",
            body=maybe_transform(
                {
                    "email": email,
                    "title": title,
                    "user_id": user_id,
                },
                v1_promote_admin_params.V1PromoteAdminParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIResponseBase,
        )


class AsyncV1Resource(AsyncAPIResource):
    @cached_property
    def users(self) -> AsyncUsersResource:
        return AsyncUsersResource(self._client)

    @cached_property
    def custom_fields(self) -> AsyncCustomFieldsResource:
        return AsyncCustomFieldsResource(self._client)

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

    async def get_custom_field_categories(
        self,
        *,
        category_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        category_names: List[str] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        order: SortOrder | NotGiven = NOT_GIVEN,
        sort: Literal["id", "name"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> V1GetCustomFieldCategoriesResponse:
        """Retrieves all custom fields categories associated with the account.

        Optionally,
        filter the results by category IDs and/or names.

        Args:
          category_ids: Custom field category ids to filter by

          category_names: Custom field category names to filter by

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
            "/users/v1/custom-field-categories",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "category_ids": category_ids,
                        "category_names": category_names,
                        "limit": limit,
                        "offset": offset,
                        "order": order,
                        "sort": sort,
                    },
                    v1_get_custom_field_categories_params.V1GetCustomFieldCategoriesParams,
                ),
            ),
            cast_to=V1GetCustomFieldCategoriesResponse,
        )

    async def get_performance_indicators(
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
    ) -> V1GetPerformanceIndicatorsResponse:
        """
        Retrieve the metric indicators of the performance data associated with account.

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
            "/users/v1/performance-indicators",
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
                    v1_get_performance_indicators_params.V1GetPerformanceIndicatorsParams,
                ),
            ),
            cast_to=V1GetPerformanceIndicatorsResponse,
        )

    async def get_smart_groups(
        self,
        *,
        id: int | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> V1GetSmartGroupsResponse:
        """
        Retrieves a list of smart groups associated with the account.

        Args:
          id: The unique identifier of the smart group.

          name: The name of the smart group to filter by.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/users/v1/smart-groups",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "id": id,
                        "name": name,
                    },
                    v1_get_smart_groups_params.V1GetSmartGroupsParams,
                ),
            ),
            cast_to=V1GetSmartGroupsResponse,
        )

    async def promote_admin(
        self,
        *,
        email: str,
        title: str,
        user_id: int,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIResponseBase:
        """Promote an existing user to an admin.

        An invitation link will be sent to the
        specified email address of the user

        Args:
          email: The email address of the user to be promoted. An invitation link will be sent to
              the specified email. Once the user acknowledges the email, the user will become
              an admin of the account.

          title: The title of the user to be promoted

          user_id: The unique identifier of the user to be promoted to admin

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/users/v1/admins",
            body=await async_maybe_transform(
                {
                    "email": email,
                    "title": title,
                    "user_id": user_id,
                },
                v1_promote_admin_params.V1PromoteAdminParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIResponseBase,
        )


class V1ResourceWithRawResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

        self.get_custom_field_categories = to_raw_response_wrapper(
            v1.get_custom_field_categories,
        )
        self.get_performance_indicators = to_raw_response_wrapper(
            v1.get_performance_indicators,
        )
        self.get_smart_groups = to_raw_response_wrapper(
            v1.get_smart_groups,
        )
        self.promote_admin = to_raw_response_wrapper(
            v1.promote_admin,
        )

    @cached_property
    def users(self) -> UsersResourceWithRawResponse:
        return UsersResourceWithRawResponse(self._v1.users)

    @cached_property
    def custom_fields(self) -> CustomFieldsResourceWithRawResponse:
        return CustomFieldsResourceWithRawResponse(self._v1.custom_fields)


class AsyncV1ResourceWithRawResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

        self.get_custom_field_categories = async_to_raw_response_wrapper(
            v1.get_custom_field_categories,
        )
        self.get_performance_indicators = async_to_raw_response_wrapper(
            v1.get_performance_indicators,
        )
        self.get_smart_groups = async_to_raw_response_wrapper(
            v1.get_smart_groups,
        )
        self.promote_admin = async_to_raw_response_wrapper(
            v1.promote_admin,
        )

    @cached_property
    def users(self) -> AsyncUsersResourceWithRawResponse:
        return AsyncUsersResourceWithRawResponse(self._v1.users)

    @cached_property
    def custom_fields(self) -> AsyncCustomFieldsResourceWithRawResponse:
        return AsyncCustomFieldsResourceWithRawResponse(self._v1.custom_fields)


class V1ResourceWithStreamingResponse:
    def __init__(self, v1: V1Resource) -> None:
        self._v1 = v1

        self.get_custom_field_categories = to_streamed_response_wrapper(
            v1.get_custom_field_categories,
        )
        self.get_performance_indicators = to_streamed_response_wrapper(
            v1.get_performance_indicators,
        )
        self.get_smart_groups = to_streamed_response_wrapper(
            v1.get_smart_groups,
        )
        self.promote_admin = to_streamed_response_wrapper(
            v1.promote_admin,
        )

    @cached_property
    def users(self) -> UsersResourceWithStreamingResponse:
        return UsersResourceWithStreamingResponse(self._v1.users)

    @cached_property
    def custom_fields(self) -> CustomFieldsResourceWithStreamingResponse:
        return CustomFieldsResourceWithStreamingResponse(self._v1.custom_fields)


class AsyncV1ResourceWithStreamingResponse:
    def __init__(self, v1: AsyncV1Resource) -> None:
        self._v1 = v1

        self.get_custom_field_categories = async_to_streamed_response_wrapper(
            v1.get_custom_field_categories,
        )
        self.get_performance_indicators = async_to_streamed_response_wrapper(
            v1.get_performance_indicators,
        )
        self.get_smart_groups = async_to_streamed_response_wrapper(
            v1.get_smart_groups,
        )
        self.promote_admin = async_to_streamed_response_wrapper(
            v1.promote_admin,
        )

    @cached_property
    def users(self) -> AsyncUsersResourceWithStreamingResponse:
        return AsyncUsersResourceWithStreamingResponse(self._v1.users)

    @cached_property
    def custom_fields(self) -> AsyncCustomFieldsResourceWithStreamingResponse:
        return AsyncCustomFieldsResourceWithStreamingResponse(self._v1.custom_fields)
