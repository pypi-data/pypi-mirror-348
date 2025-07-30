# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from connecteam_api_sdk import ConnecteamAPISDK, AsyncConnecteamAPISDK
from connecteam_api_sdk.types.scheduler.v1.schedulers.shifts import (
    AutoAssignGetStatusResponse,
    AutoAssignCreateRequestResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAutoAssign:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_request(self, client: ConnecteamAPISDK) -> None:
        auto_assign = client.scheduler.v1.schedulers.shifts.auto_assign.create_request(
            scheduler_id=0,
            shifts_ids=["string"],
        )
        assert_matches_type(AutoAssignCreateRequestResponse, auto_assign, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_request_with_all_params(self, client: ConnecteamAPISDK) -> None:
        auto_assign = client.scheduler.v1.schedulers.shifts.auto_assign.create_request(
            scheduler_id=0,
            shifts_ids=["string"],
            is_force_limitations=True,
            is_force_open_shift_requests=True,
            is_force_qualification=True,
            is_force_unavailability=True,
        )
        assert_matches_type(AutoAssignCreateRequestResponse, auto_assign, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_request(self, client: ConnecteamAPISDK) -> None:
        response = client.scheduler.v1.schedulers.shifts.auto_assign.with_raw_response.create_request(
            scheduler_id=0,
            shifts_ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        auto_assign = response.parse()
        assert_matches_type(AutoAssignCreateRequestResponse, auto_assign, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_request(self, client: ConnecteamAPISDK) -> None:
        with client.scheduler.v1.schedulers.shifts.auto_assign.with_streaming_response.create_request(
            scheduler_id=0,
            shifts_ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            auto_assign = response.parse()
            assert_matches_type(AutoAssignCreateRequestResponse, auto_assign, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_get_status(self, client: ConnecteamAPISDK) -> None:
        auto_assign = client.scheduler.v1.schedulers.shifts.auto_assign.get_status(
            auto_assign_request_id=0,
            scheduler_id=0,
        )
        assert_matches_type(AutoAssignGetStatusResponse, auto_assign, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_status(self, client: ConnecteamAPISDK) -> None:
        response = client.scheduler.v1.schedulers.shifts.auto_assign.with_raw_response.get_status(
            auto_assign_request_id=0,
            scheduler_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        auto_assign = response.parse()
        assert_matches_type(AutoAssignGetStatusResponse, auto_assign, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_status(self, client: ConnecteamAPISDK) -> None:
        with client.scheduler.v1.schedulers.shifts.auto_assign.with_streaming_response.get_status(
            auto_assign_request_id=0,
            scheduler_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            auto_assign = response.parse()
            assert_matches_type(AutoAssignGetStatusResponse, auto_assign, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAutoAssign:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_request(self, async_client: AsyncConnecteamAPISDK) -> None:
        auto_assign = await async_client.scheduler.v1.schedulers.shifts.auto_assign.create_request(
            scheduler_id=0,
            shifts_ids=["string"],
        )
        assert_matches_type(AutoAssignCreateRequestResponse, auto_assign, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_request_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        auto_assign = await async_client.scheduler.v1.schedulers.shifts.auto_assign.create_request(
            scheduler_id=0,
            shifts_ids=["string"],
            is_force_limitations=True,
            is_force_open_shift_requests=True,
            is_force_qualification=True,
            is_force_unavailability=True,
        )
        assert_matches_type(AutoAssignCreateRequestResponse, auto_assign, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_request(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.scheduler.v1.schedulers.shifts.auto_assign.with_raw_response.create_request(
            scheduler_id=0,
            shifts_ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        auto_assign = await response.parse()
        assert_matches_type(AutoAssignCreateRequestResponse, auto_assign, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_request(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.scheduler.v1.schedulers.shifts.auto_assign.with_streaming_response.create_request(
            scheduler_id=0,
            shifts_ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            auto_assign = await response.parse()
            assert_matches_type(AutoAssignCreateRequestResponse, auto_assign, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_status(self, async_client: AsyncConnecteamAPISDK) -> None:
        auto_assign = await async_client.scheduler.v1.schedulers.shifts.auto_assign.get_status(
            auto_assign_request_id=0,
            scheduler_id=0,
        )
        assert_matches_type(AutoAssignGetStatusResponse, auto_assign, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_status(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.scheduler.v1.schedulers.shifts.auto_assign.with_raw_response.get_status(
            auto_assign_request_id=0,
            scheduler_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        auto_assign = await response.parse()
        assert_matches_type(AutoAssignGetStatusResponse, auto_assign, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_status(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.scheduler.v1.schedulers.shifts.auto_assign.with_streaming_response.get_status(
            auto_assign_request_id=0,
            scheduler_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            auto_assign = await response.parse()
            assert_matches_type(AutoAssignGetStatusResponse, auto_assign, path=["response"])

        assert cast(Any, response.is_closed) is True
