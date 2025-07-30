# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from connecteam_api_sdk import ConnecteamAPISDK, AsyncConnecteamAPISDK
from connecteam_api_sdk.types.time_off import V1CreateRequestResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestV1:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_request(self, client: ConnecteamAPISDK) -> None:
        v1 = client.time_off.v1.create_request(
            end_date="endDate",
            is_all_day=True,
            policy_type_id="policyTypeId",
            start_date="startDate",
            status="approved",
            timezone="timezone",
            user_id=1,
        )
        assert_matches_type(V1CreateRequestResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_request_with_all_params(self, client: ConnecteamAPISDK) -> None:
        v1 = client.time_off.v1.create_request(
            end_date="endDate",
            is_all_day=True,
            policy_type_id="policyTypeId",
            start_date="startDate",
            status="approved",
            timezone="timezone",
            user_id=1,
            employee_note="employeeNote",
            end_time="endTime",
            is_adjust_for_day_light_saving=True,
            manager_note="managerNote",
            start_time="startTime",
            time_clock_id=0,
        )
        assert_matches_type(V1CreateRequestResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_request(self, client: ConnecteamAPISDK) -> None:
        response = client.time_off.v1.with_raw_response.create_request(
            end_date="endDate",
            is_all_day=True,
            policy_type_id="policyTypeId",
            start_date="startDate",
            status="approved",
            timezone="timezone",
            user_id=1,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = response.parse()
        assert_matches_type(V1CreateRequestResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_request(self, client: ConnecteamAPISDK) -> None:
        with client.time_off.v1.with_streaming_response.create_request(
            end_date="endDate",
            is_all_day=True,
            policy_type_id="policyTypeId",
            start_date="startDate",
            status="approved",
            timezone="timezone",
            user_id=1,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = response.parse()
            assert_matches_type(V1CreateRequestResponse, v1, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncV1:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_request(self, async_client: AsyncConnecteamAPISDK) -> None:
        v1 = await async_client.time_off.v1.create_request(
            end_date="endDate",
            is_all_day=True,
            policy_type_id="policyTypeId",
            start_date="startDate",
            status="approved",
            timezone="timezone",
            user_id=1,
        )
        assert_matches_type(V1CreateRequestResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_request_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        v1 = await async_client.time_off.v1.create_request(
            end_date="endDate",
            is_all_day=True,
            policy_type_id="policyTypeId",
            start_date="startDate",
            status="approved",
            timezone="timezone",
            user_id=1,
            employee_note="employeeNote",
            end_time="endTime",
            is_adjust_for_day_light_saving=True,
            manager_note="managerNote",
            start_time="startTime",
            time_clock_id=0,
        )
        assert_matches_type(V1CreateRequestResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_request(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.time_off.v1.with_raw_response.create_request(
            end_date="endDate",
            is_all_day=True,
            policy_type_id="policyTypeId",
            start_date="startDate",
            status="approved",
            timezone="timezone",
            user_id=1,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = await response.parse()
        assert_matches_type(V1CreateRequestResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_request(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.time_off.v1.with_streaming_response.create_request(
            end_date="endDate",
            is_all_day=True,
            policy_type_id="policyTypeId",
            start_date="startDate",
            status="approved",
            timezone="timezone",
            user_id=1,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = await response.parse()
            assert_matches_type(V1CreateRequestResponse, v1, path=["response"])

        assert cast(Any, response.is_closed) is True
