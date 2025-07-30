# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .balances import (
    BalancesResource,
    AsyncBalancesResource,
    BalancesResourceWithRawResponse,
    AsyncBalancesResourceWithRawResponse,
    BalancesResourceWithStreamingResponse,
    AsyncBalancesResourceWithStreamingResponse,
)
from ....._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....._base_client import make_request_options
from .....types.time_off.v1.policy_type_list_response import PolicyTypeListResponse

__all__ = ["PolicyTypesResource", "AsyncPolicyTypesResource"]


class PolicyTypesResource(SyncAPIResource):
    @cached_property
    def balances(self) -> BalancesResource:
        return BalancesResource(self._client)

    @cached_property
    def with_raw_response(self) -> PolicyTypesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return PolicyTypesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PolicyTypesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return PolicyTypesResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PolicyTypeListResponse:
        """Retrieve a list of policy types associated with the account"""
        return self._get(
            "/time-off/v1/policy-types",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PolicyTypeListResponse,
        )


class AsyncPolicyTypesResource(AsyncAPIResource):
    @cached_property
    def balances(self) -> AsyncBalancesResource:
        return AsyncBalancesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncPolicyTypesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPolicyTypesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPolicyTypesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return AsyncPolicyTypesResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PolicyTypeListResponse:
        """Retrieve a list of policy types associated with the account"""
        return await self._get(
            "/time-off/v1/policy-types",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PolicyTypeListResponse,
        )


class PolicyTypesResourceWithRawResponse:
    def __init__(self, policy_types: PolicyTypesResource) -> None:
        self._policy_types = policy_types

        self.list = to_raw_response_wrapper(
            policy_types.list,
        )

    @cached_property
    def balances(self) -> BalancesResourceWithRawResponse:
        return BalancesResourceWithRawResponse(self._policy_types.balances)


class AsyncPolicyTypesResourceWithRawResponse:
    def __init__(self, policy_types: AsyncPolicyTypesResource) -> None:
        self._policy_types = policy_types

        self.list = async_to_raw_response_wrapper(
            policy_types.list,
        )

    @cached_property
    def balances(self) -> AsyncBalancesResourceWithRawResponse:
        return AsyncBalancesResourceWithRawResponse(self._policy_types.balances)


class PolicyTypesResourceWithStreamingResponse:
    def __init__(self, policy_types: PolicyTypesResource) -> None:
        self._policy_types = policy_types

        self.list = to_streamed_response_wrapper(
            policy_types.list,
        )

    @cached_property
    def balances(self) -> BalancesResourceWithStreamingResponse:
        return BalancesResourceWithStreamingResponse(self._policy_types.balances)


class AsyncPolicyTypesResourceWithStreamingResponse:
    def __init__(self, policy_types: AsyncPolicyTypesResource) -> None:
        self._policy_types = policy_types

        self.list = async_to_streamed_response_wrapper(
            policy_types.list,
        )

    @cached_property
    def balances(self) -> AsyncBalancesResourceWithStreamingResponse:
        return AsyncBalancesResourceWithStreamingResponse(self._policy_types.balances)
