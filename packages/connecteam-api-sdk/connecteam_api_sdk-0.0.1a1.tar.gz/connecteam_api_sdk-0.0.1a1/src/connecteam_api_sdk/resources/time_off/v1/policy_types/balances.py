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
from .....types.time_off.v1.policy_types import balance_list_params, balance_update_params
from .....types.time_off.v1.policy_types.balance_list_response import BalanceListResponse
from .....types.time_off.v1.policy_types.balance_update_response import BalanceUpdateResponse

__all__ = ["BalancesResource", "AsyncBalancesResource"]


class BalancesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> BalancesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return BalancesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BalancesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return BalancesResourceWithStreamingResponse(self)

    def update(
        self,
        user_id: int,
        *,
        policy_type_id: str,
        balance: float,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BalanceUpdateResponse:
        """
        Update user time-off balance within a policy type

        Args:
          policy_type_id: Policy type id

          user_id: The ID of the user to update balance

          balance: The balance to update to

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not policy_type_id:
            raise ValueError(f"Expected a non-empty value for `policy_type_id` but received {policy_type_id!r}")
        return self._put(
            f"/time-off/v1/policy-types/{policy_type_id}/balances/{user_id}",
            body=maybe_transform({"balance": balance}, balance_update_params.BalanceUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BalanceUpdateResponse,
        )

    def list(
        self,
        policy_type_id: str,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        user_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BalanceListResponse:
        """
        Retrieve a list of user time-off balances within a policy type

        Args:
          policy_type_id: Policy type id

          limit: The maximum number of results to display per page

          offset: The resource offset of the last successfully read resource will be returned as
              the paging.offset JSON property of a paginated response containing more results

          user_ids: List of user ids

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not policy_type_id:
            raise ValueError(f"Expected a non-empty value for `policy_type_id` but received {policy_type_id!r}")
        return self._get(
            f"/time-off/v1/policy-types/{policy_type_id}/balances",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                        "user_ids": user_ids,
                    },
                    balance_list_params.BalanceListParams,
                ),
            ),
            cast_to=BalanceListResponse,
        )


class AsyncBalancesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncBalancesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncBalancesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBalancesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return AsyncBalancesResourceWithStreamingResponse(self)

    async def update(
        self,
        user_id: int,
        *,
        policy_type_id: str,
        balance: float,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BalanceUpdateResponse:
        """
        Update user time-off balance within a policy type

        Args:
          policy_type_id: Policy type id

          user_id: The ID of the user to update balance

          balance: The balance to update to

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not policy_type_id:
            raise ValueError(f"Expected a non-empty value for `policy_type_id` but received {policy_type_id!r}")
        return await self._put(
            f"/time-off/v1/policy-types/{policy_type_id}/balances/{user_id}",
            body=await async_maybe_transform({"balance": balance}, balance_update_params.BalanceUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BalanceUpdateResponse,
        )

    async def list(
        self,
        policy_type_id: str,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        user_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BalanceListResponse:
        """
        Retrieve a list of user time-off balances within a policy type

        Args:
          policy_type_id: Policy type id

          limit: The maximum number of results to display per page

          offset: The resource offset of the last successfully read resource will be returned as
              the paging.offset JSON property of a paginated response containing more results

          user_ids: List of user ids

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not policy_type_id:
            raise ValueError(f"Expected a non-empty value for `policy_type_id` but received {policy_type_id!r}")
        return await self._get(
            f"/time-off/v1/policy-types/{policy_type_id}/balances",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                        "user_ids": user_ids,
                    },
                    balance_list_params.BalanceListParams,
                ),
            ),
            cast_to=BalanceListResponse,
        )


class BalancesResourceWithRawResponse:
    def __init__(self, balances: BalancesResource) -> None:
        self._balances = balances

        self.update = to_raw_response_wrapper(
            balances.update,
        )
        self.list = to_raw_response_wrapper(
            balances.list,
        )


class AsyncBalancesResourceWithRawResponse:
    def __init__(self, balances: AsyncBalancesResource) -> None:
        self._balances = balances

        self.update = async_to_raw_response_wrapper(
            balances.update,
        )
        self.list = async_to_raw_response_wrapper(
            balances.list,
        )


class BalancesResourceWithStreamingResponse:
    def __init__(self, balances: BalancesResource) -> None:
        self._balances = balances

        self.update = to_streamed_response_wrapper(
            balances.update,
        )
        self.list = to_streamed_response_wrapper(
            balances.list,
        )


class AsyncBalancesResourceWithStreamingResponse:
    def __init__(self, balances: AsyncBalancesResource) -> None:
        self._balances = balances

        self.update = async_to_streamed_response_wrapper(
            balances.update,
        )
        self.list = async_to_streamed_response_wrapper(
            balances.list,
        )
