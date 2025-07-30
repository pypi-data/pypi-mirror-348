# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from connecteam_api_sdk import ConnecteamAPISDK, AsyncConnecteamAPISDK
from connecteam_api_sdk.types.time_clock.v1 import (
    TimeClockListResponse,
    TimeClockClockInResponse,
    TimeClockClockOutResponse,
    TimeClockGetManualBreaksResponse,
    TimeClockGetShiftAttachmentsResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTimeClocks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: ConnecteamAPISDK) -> None:
        time_clock = client.time_clock.v1.time_clocks.list()
        assert_matches_type(TimeClockListResponse, time_clock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: ConnecteamAPISDK) -> None:
        response = client.time_clock.v1.time_clocks.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        time_clock = response.parse()
        assert_matches_type(TimeClockListResponse, time_clock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: ConnecteamAPISDK) -> None:
        with client.time_clock.v1.time_clocks.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            time_clock = response.parse()
            assert_matches_type(TimeClockListResponse, time_clock, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_clock_in(self, client: ConnecteamAPISDK) -> None:
        time_clock = client.time_clock.v1.time_clocks.clock_in(
            time_clock_id=0,
            job_id="jobId",
            user_id=0,
        )
        assert_matches_type(TimeClockClockInResponse, time_clock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_clock_in_with_all_params(self, client: ConnecteamAPISDK) -> None:
        time_clock = client.time_clock.v1.time_clocks.clock_in(
            time_clock_id=0,
            job_id="jobId",
            user_id=0,
            location_data={
                "address": "address",
                "latitude": 0,
                "longitude": 0,
            },
            scheduler_shift_id="schedulerShiftId",
            timezone="timezone",
        )
        assert_matches_type(TimeClockClockInResponse, time_clock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_clock_in(self, client: ConnecteamAPISDK) -> None:
        response = client.time_clock.v1.time_clocks.with_raw_response.clock_in(
            time_clock_id=0,
            job_id="jobId",
            user_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        time_clock = response.parse()
        assert_matches_type(TimeClockClockInResponse, time_clock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_clock_in(self, client: ConnecteamAPISDK) -> None:
        with client.time_clock.v1.time_clocks.with_streaming_response.clock_in(
            time_clock_id=0,
            job_id="jobId",
            user_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            time_clock = response.parse()
            assert_matches_type(TimeClockClockInResponse, time_clock, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_clock_out(self, client: ConnecteamAPISDK) -> None:
        time_clock = client.time_clock.v1.time_clocks.clock_out(
            time_clock_id=0,
            user_id=0,
        )
        assert_matches_type(TimeClockClockOutResponse, time_clock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_clock_out_with_all_params(self, client: ConnecteamAPISDK) -> None:
        time_clock = client.time_clock.v1.time_clocks.clock_out(
            time_clock_id=0,
            user_id=0,
            location_data={
                "address": "address",
                "latitude": 0,
                "longitude": 0,
            },
            timezone="timezone",
        )
        assert_matches_type(TimeClockClockOutResponse, time_clock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_clock_out(self, client: ConnecteamAPISDK) -> None:
        response = client.time_clock.v1.time_clocks.with_raw_response.clock_out(
            time_clock_id=0,
            user_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        time_clock = response.parse()
        assert_matches_type(TimeClockClockOutResponse, time_clock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_clock_out(self, client: ConnecteamAPISDK) -> None:
        with client.time_clock.v1.time_clocks.with_streaming_response.clock_out(
            time_clock_id=0,
            user_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            time_clock = response.parse()
            assert_matches_type(TimeClockClockOutResponse, time_clock, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_get_manual_breaks(self, client: ConnecteamAPISDK) -> None:
        time_clock = client.time_clock.v1.time_clocks.get_manual_breaks(
            0,
        )
        assert_matches_type(TimeClockGetManualBreaksResponse, time_clock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_manual_breaks(self, client: ConnecteamAPISDK) -> None:
        response = client.time_clock.v1.time_clocks.with_raw_response.get_manual_breaks(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        time_clock = response.parse()
        assert_matches_type(TimeClockGetManualBreaksResponse, time_clock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_manual_breaks(self, client: ConnecteamAPISDK) -> None:
        with client.time_clock.v1.time_clocks.with_streaming_response.get_manual_breaks(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            time_clock = response.parse()
            assert_matches_type(TimeClockGetManualBreaksResponse, time_clock, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_get_shift_attachments(self, client: ConnecteamAPISDK) -> None:
        time_clock = client.time_clock.v1.time_clocks.get_shift_attachments(
            0,
        )
        assert_matches_type(TimeClockGetShiftAttachmentsResponse, time_clock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_shift_attachments(self, client: ConnecteamAPISDK) -> None:
        response = client.time_clock.v1.time_clocks.with_raw_response.get_shift_attachments(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        time_clock = response.parse()
        assert_matches_type(TimeClockGetShiftAttachmentsResponse, time_clock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_shift_attachments(self, client: ConnecteamAPISDK) -> None:
        with client.time_clock.v1.time_clocks.with_streaming_response.get_shift_attachments(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            time_clock = response.parse()
            assert_matches_type(TimeClockGetShiftAttachmentsResponse, time_clock, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncTimeClocks:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        time_clock = await async_client.time_clock.v1.time_clocks.list()
        assert_matches_type(TimeClockListResponse, time_clock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.time_clock.v1.time_clocks.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        time_clock = await response.parse()
        assert_matches_type(TimeClockListResponse, time_clock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.time_clock.v1.time_clocks.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            time_clock = await response.parse()
            assert_matches_type(TimeClockListResponse, time_clock, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_clock_in(self, async_client: AsyncConnecteamAPISDK) -> None:
        time_clock = await async_client.time_clock.v1.time_clocks.clock_in(
            time_clock_id=0,
            job_id="jobId",
            user_id=0,
        )
        assert_matches_type(TimeClockClockInResponse, time_clock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_clock_in_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        time_clock = await async_client.time_clock.v1.time_clocks.clock_in(
            time_clock_id=0,
            job_id="jobId",
            user_id=0,
            location_data={
                "address": "address",
                "latitude": 0,
                "longitude": 0,
            },
            scheduler_shift_id="schedulerShiftId",
            timezone="timezone",
        )
        assert_matches_type(TimeClockClockInResponse, time_clock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_clock_in(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.time_clock.v1.time_clocks.with_raw_response.clock_in(
            time_clock_id=0,
            job_id="jobId",
            user_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        time_clock = await response.parse()
        assert_matches_type(TimeClockClockInResponse, time_clock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_clock_in(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.time_clock.v1.time_clocks.with_streaming_response.clock_in(
            time_clock_id=0,
            job_id="jobId",
            user_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            time_clock = await response.parse()
            assert_matches_type(TimeClockClockInResponse, time_clock, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_clock_out(self, async_client: AsyncConnecteamAPISDK) -> None:
        time_clock = await async_client.time_clock.v1.time_clocks.clock_out(
            time_clock_id=0,
            user_id=0,
        )
        assert_matches_type(TimeClockClockOutResponse, time_clock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_clock_out_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        time_clock = await async_client.time_clock.v1.time_clocks.clock_out(
            time_clock_id=0,
            user_id=0,
            location_data={
                "address": "address",
                "latitude": 0,
                "longitude": 0,
            },
            timezone="timezone",
        )
        assert_matches_type(TimeClockClockOutResponse, time_clock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_clock_out(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.time_clock.v1.time_clocks.with_raw_response.clock_out(
            time_clock_id=0,
            user_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        time_clock = await response.parse()
        assert_matches_type(TimeClockClockOutResponse, time_clock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_clock_out(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.time_clock.v1.time_clocks.with_streaming_response.clock_out(
            time_clock_id=0,
            user_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            time_clock = await response.parse()
            assert_matches_type(TimeClockClockOutResponse, time_clock, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_manual_breaks(self, async_client: AsyncConnecteamAPISDK) -> None:
        time_clock = await async_client.time_clock.v1.time_clocks.get_manual_breaks(
            0,
        )
        assert_matches_type(TimeClockGetManualBreaksResponse, time_clock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_manual_breaks(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.time_clock.v1.time_clocks.with_raw_response.get_manual_breaks(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        time_clock = await response.parse()
        assert_matches_type(TimeClockGetManualBreaksResponse, time_clock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_manual_breaks(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.time_clock.v1.time_clocks.with_streaming_response.get_manual_breaks(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            time_clock = await response.parse()
            assert_matches_type(TimeClockGetManualBreaksResponse, time_clock, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_shift_attachments(self, async_client: AsyncConnecteamAPISDK) -> None:
        time_clock = await async_client.time_clock.v1.time_clocks.get_shift_attachments(
            0,
        )
        assert_matches_type(TimeClockGetShiftAttachmentsResponse, time_clock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_shift_attachments(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.time_clock.v1.time_clocks.with_raw_response.get_shift_attachments(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        time_clock = await response.parse()
        assert_matches_type(TimeClockGetShiftAttachmentsResponse, time_clock, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_shift_attachments(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.time_clock.v1.time_clocks.with_streaming_response.get_shift_attachments(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            time_clock = await response.parse()
            assert_matches_type(TimeClockGetShiftAttachmentsResponse, time_clock, path=["response"])

        assert cast(Any, response.is_closed) is True
