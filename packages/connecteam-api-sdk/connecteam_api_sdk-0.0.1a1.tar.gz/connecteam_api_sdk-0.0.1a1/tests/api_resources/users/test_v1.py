# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from connecteam_api_sdk import ConnecteamAPISDK, AsyncConnecteamAPISDK
from connecteam_api_sdk.types.users import (
    V1GetSmartGroupsResponse,
    V1GetCustomFieldCategoriesResponse,
    V1GetPerformanceIndicatorsResponse,
)
from connecteam_api_sdk.types.users.v1.custom_fields import APIResponseBase

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestV1:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_get_custom_field_categories(self, client: ConnecteamAPISDK) -> None:
        v1 = client.users.v1.get_custom_field_categories()
        assert_matches_type(V1GetCustomFieldCategoriesResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_get_custom_field_categories_with_all_params(self, client: ConnecteamAPISDK) -> None:
        v1 = client.users.v1.get_custom_field_categories(
            category_ids=[0],
            category_names=["string"],
            limit=1,
            offset=0,
            order="asc",
            sort="id",
        )
        assert_matches_type(V1GetCustomFieldCategoriesResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_custom_field_categories(self, client: ConnecteamAPISDK) -> None:
        response = client.users.v1.with_raw_response.get_custom_field_categories()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = response.parse()
        assert_matches_type(V1GetCustomFieldCategoriesResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_custom_field_categories(self, client: ConnecteamAPISDK) -> None:
        with client.users.v1.with_streaming_response.get_custom_field_categories() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = response.parse()
            assert_matches_type(V1GetCustomFieldCategoriesResponse, v1, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_get_performance_indicators(self, client: ConnecteamAPISDK) -> None:
        v1 = client.users.v1.get_performance_indicators()
        assert_matches_type(V1GetPerformanceIndicatorsResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_get_performance_indicators_with_all_params(self, client: ConnecteamAPISDK) -> None:
        v1 = client.users.v1.get_performance_indicators(
            limit=1,
            offset=0,
        )
        assert_matches_type(V1GetPerformanceIndicatorsResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_performance_indicators(self, client: ConnecteamAPISDK) -> None:
        response = client.users.v1.with_raw_response.get_performance_indicators()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = response.parse()
        assert_matches_type(V1GetPerformanceIndicatorsResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_performance_indicators(self, client: ConnecteamAPISDK) -> None:
        with client.users.v1.with_streaming_response.get_performance_indicators() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = response.parse()
            assert_matches_type(V1GetPerformanceIndicatorsResponse, v1, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_get_smart_groups(self, client: ConnecteamAPISDK) -> None:
        v1 = client.users.v1.get_smart_groups()
        assert_matches_type(V1GetSmartGroupsResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_get_smart_groups_with_all_params(self, client: ConnecteamAPISDK) -> None:
        v1 = client.users.v1.get_smart_groups(
            id=0,
            name="name",
        )
        assert_matches_type(V1GetSmartGroupsResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_smart_groups(self, client: ConnecteamAPISDK) -> None:
        response = client.users.v1.with_raw_response.get_smart_groups()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = response.parse()
        assert_matches_type(V1GetSmartGroupsResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_smart_groups(self, client: ConnecteamAPISDK) -> None:
        with client.users.v1.with_streaming_response.get_smart_groups() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = response.parse()
            assert_matches_type(V1GetSmartGroupsResponse, v1, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_promote_admin(self, client: ConnecteamAPISDK) -> None:
        v1 = client.users.v1.promote_admin(
            email="email",
            title="title",
            user_id=1,
        )
        assert_matches_type(APIResponseBase, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_promote_admin(self, client: ConnecteamAPISDK) -> None:
        response = client.users.v1.with_raw_response.promote_admin(
            email="email",
            title="title",
            user_id=1,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = response.parse()
        assert_matches_type(APIResponseBase, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_promote_admin(self, client: ConnecteamAPISDK) -> None:
        with client.users.v1.with_streaming_response.promote_admin(
            email="email",
            title="title",
            user_id=1,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = response.parse()
            assert_matches_type(APIResponseBase, v1, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncV1:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_custom_field_categories(self, async_client: AsyncConnecteamAPISDK) -> None:
        v1 = await async_client.users.v1.get_custom_field_categories()
        assert_matches_type(V1GetCustomFieldCategoriesResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_custom_field_categories_with_all_params(
        self, async_client: AsyncConnecteamAPISDK
    ) -> None:
        v1 = await async_client.users.v1.get_custom_field_categories(
            category_ids=[0],
            category_names=["string"],
            limit=1,
            offset=0,
            order="asc",
            sort="id",
        )
        assert_matches_type(V1GetCustomFieldCategoriesResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_custom_field_categories(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.users.v1.with_raw_response.get_custom_field_categories()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = await response.parse()
        assert_matches_type(V1GetCustomFieldCategoriesResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_custom_field_categories(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.users.v1.with_streaming_response.get_custom_field_categories() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = await response.parse()
            assert_matches_type(V1GetCustomFieldCategoriesResponse, v1, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_performance_indicators(self, async_client: AsyncConnecteamAPISDK) -> None:
        v1 = await async_client.users.v1.get_performance_indicators()
        assert_matches_type(V1GetPerformanceIndicatorsResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_performance_indicators_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        v1 = await async_client.users.v1.get_performance_indicators(
            limit=1,
            offset=0,
        )
        assert_matches_type(V1GetPerformanceIndicatorsResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_performance_indicators(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.users.v1.with_raw_response.get_performance_indicators()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = await response.parse()
        assert_matches_type(V1GetPerformanceIndicatorsResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_performance_indicators(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.users.v1.with_streaming_response.get_performance_indicators() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = await response.parse()
            assert_matches_type(V1GetPerformanceIndicatorsResponse, v1, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_smart_groups(self, async_client: AsyncConnecteamAPISDK) -> None:
        v1 = await async_client.users.v1.get_smart_groups()
        assert_matches_type(V1GetSmartGroupsResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_smart_groups_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        v1 = await async_client.users.v1.get_smart_groups(
            id=0,
            name="name",
        )
        assert_matches_type(V1GetSmartGroupsResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_smart_groups(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.users.v1.with_raw_response.get_smart_groups()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = await response.parse()
        assert_matches_type(V1GetSmartGroupsResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_smart_groups(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.users.v1.with_streaming_response.get_smart_groups() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = await response.parse()
            assert_matches_type(V1GetSmartGroupsResponse, v1, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_promote_admin(self, async_client: AsyncConnecteamAPISDK) -> None:
        v1 = await async_client.users.v1.promote_admin(
            email="email",
            title="title",
            user_id=1,
        )
        assert_matches_type(APIResponseBase, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_promote_admin(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.users.v1.with_raw_response.promote_admin(
            email="email",
            title="title",
            user_id=1,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = await response.parse()
        assert_matches_type(APIResponseBase, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_promote_admin(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.users.v1.with_streaming_response.promote_admin(
            email="email",
            title="title",
            user_id=1,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = await response.parse()
            assert_matches_type(APIResponseBase, v1, path=["response"])

        assert cast(Any, response.is_closed) is True
