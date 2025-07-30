# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from connecteam_api_sdk import ConnecteamAPISDK, AsyncConnecteamAPISDK
from connecteam_api_sdk.types.time_off.v1.policy_types import (
    BalanceListResponse,
    BalanceUpdateResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestBalances:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: ConnecteamAPISDK) -> None:
        balance = client.time_off.v1.policy_types.balances.update(
            user_id=1,
            policy_type_id="policyTypeId",
            balance=0,
        )
        assert_matches_type(BalanceUpdateResponse, balance, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: ConnecteamAPISDK) -> None:
        response = client.time_off.v1.policy_types.balances.with_raw_response.update(
            user_id=1,
            policy_type_id="policyTypeId",
            balance=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        balance = response.parse()
        assert_matches_type(BalanceUpdateResponse, balance, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: ConnecteamAPISDK) -> None:
        with client.time_off.v1.policy_types.balances.with_streaming_response.update(
            user_id=1,
            policy_type_id="policyTypeId",
            balance=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            balance = response.parse()
            assert_matches_type(BalanceUpdateResponse, balance, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: ConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `policy_type_id` but received ''"):
            client.time_off.v1.policy_types.balances.with_raw_response.update(
                user_id=1,
                policy_type_id="",
                balance=0,
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: ConnecteamAPISDK) -> None:
        balance = client.time_off.v1.policy_types.balances.list(
            policy_type_id="policyTypeId",
        )
        assert_matches_type(BalanceListResponse, balance, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: ConnecteamAPISDK) -> None:
        balance = client.time_off.v1.policy_types.balances.list(
            policy_type_id="policyTypeId",
            limit=1,
            offset=0,
            user_ids=[1],
        )
        assert_matches_type(BalanceListResponse, balance, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: ConnecteamAPISDK) -> None:
        response = client.time_off.v1.policy_types.balances.with_raw_response.list(
            policy_type_id="policyTypeId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        balance = response.parse()
        assert_matches_type(BalanceListResponse, balance, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: ConnecteamAPISDK) -> None:
        with client.time_off.v1.policy_types.balances.with_streaming_response.list(
            policy_type_id="policyTypeId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            balance = response.parse()
            assert_matches_type(BalanceListResponse, balance, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_list(self, client: ConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `policy_type_id` but received ''"):
            client.time_off.v1.policy_types.balances.with_raw_response.list(
                policy_type_id="",
            )


class TestAsyncBalances:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        balance = await async_client.time_off.v1.policy_types.balances.update(
            user_id=1,
            policy_type_id="policyTypeId",
            balance=0,
        )
        assert_matches_type(BalanceUpdateResponse, balance, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.time_off.v1.policy_types.balances.with_raw_response.update(
            user_id=1,
            policy_type_id="policyTypeId",
            balance=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        balance = await response.parse()
        assert_matches_type(BalanceUpdateResponse, balance, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.time_off.v1.policy_types.balances.with_streaming_response.update(
            user_id=1,
            policy_type_id="policyTypeId",
            balance=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            balance = await response.parse()
            assert_matches_type(BalanceUpdateResponse, balance, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `policy_type_id` but received ''"):
            await async_client.time_off.v1.policy_types.balances.with_raw_response.update(
                user_id=1,
                policy_type_id="",
                balance=0,
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        balance = await async_client.time_off.v1.policy_types.balances.list(
            policy_type_id="policyTypeId",
        )
        assert_matches_type(BalanceListResponse, balance, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        balance = await async_client.time_off.v1.policy_types.balances.list(
            policy_type_id="policyTypeId",
            limit=1,
            offset=0,
            user_ids=[1],
        )
        assert_matches_type(BalanceListResponse, balance, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.time_off.v1.policy_types.balances.with_raw_response.list(
            policy_type_id="policyTypeId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        balance = await response.parse()
        assert_matches_type(BalanceListResponse, balance, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.time_off.v1.policy_types.balances.with_streaming_response.list(
            policy_type_id="policyTypeId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            balance = await response.parse()
            assert_matches_type(BalanceListResponse, balance, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `policy_type_id` but received ''"):
            await async_client.time_off.v1.policy_types.balances.with_raw_response.list(
                policy_type_id="",
            )
