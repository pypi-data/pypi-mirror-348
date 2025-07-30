# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from connecteam_api_sdk import ConnecteamAPISDK, AsyncConnecteamAPISDK
from connecteam_api_sdk.types.scheduler.v1 import (
    SchedulerListResponse,
    SchedulerGetUserUnavailabilitiesResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSchedulers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: ConnecteamAPISDK) -> None:
        scheduler = client.scheduler.v1.schedulers.list()
        assert_matches_type(SchedulerListResponse, scheduler, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: ConnecteamAPISDK) -> None:
        response = client.scheduler.v1.schedulers.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scheduler = response.parse()
        assert_matches_type(SchedulerListResponse, scheduler, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: ConnecteamAPISDK) -> None:
        with client.scheduler.v1.schedulers.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scheduler = response.parse()
            assert_matches_type(SchedulerListResponse, scheduler, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_get_user_unavailabilities(self, client: ConnecteamAPISDK) -> None:
        scheduler = client.scheduler.v1.schedulers.get_user_unavailabilities(
            end_time=1,
            start_time=1,
            user_id=0,
        )
        assert_matches_type(SchedulerGetUserUnavailabilitiesResponse, scheduler, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_user_unavailabilities(self, client: ConnecteamAPISDK) -> None:
        response = client.scheduler.v1.schedulers.with_raw_response.get_user_unavailabilities(
            end_time=1,
            start_time=1,
            user_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scheduler = response.parse()
        assert_matches_type(SchedulerGetUserUnavailabilitiesResponse, scheduler, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_user_unavailabilities(self, client: ConnecteamAPISDK) -> None:
        with client.scheduler.v1.schedulers.with_streaming_response.get_user_unavailabilities(
            end_time=1,
            start_time=1,
            user_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scheduler = response.parse()
            assert_matches_type(SchedulerGetUserUnavailabilitiesResponse, scheduler, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSchedulers:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        scheduler = await async_client.scheduler.v1.schedulers.list()
        assert_matches_type(SchedulerListResponse, scheduler, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.scheduler.v1.schedulers.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scheduler = await response.parse()
        assert_matches_type(SchedulerListResponse, scheduler, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.scheduler.v1.schedulers.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scheduler = await response.parse()
            assert_matches_type(SchedulerListResponse, scheduler, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_user_unavailabilities(self, async_client: AsyncConnecteamAPISDK) -> None:
        scheduler = await async_client.scheduler.v1.schedulers.get_user_unavailabilities(
            end_time=1,
            start_time=1,
            user_id=0,
        )
        assert_matches_type(SchedulerGetUserUnavailabilitiesResponse, scheduler, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_user_unavailabilities(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.scheduler.v1.schedulers.with_raw_response.get_user_unavailabilities(
            end_time=1,
            start_time=1,
            user_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        scheduler = await response.parse()
        assert_matches_type(SchedulerGetUserUnavailabilitiesResponse, scheduler, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_user_unavailabilities(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.scheduler.v1.schedulers.with_streaming_response.get_user_unavailabilities(
            end_time=1,
            start_time=1,
            user_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            scheduler = await response.parse()
            assert_matches_type(SchedulerGetUserUnavailabilitiesResponse, scheduler, path=["response"])

        assert cast(Any, response.is_closed) is True
