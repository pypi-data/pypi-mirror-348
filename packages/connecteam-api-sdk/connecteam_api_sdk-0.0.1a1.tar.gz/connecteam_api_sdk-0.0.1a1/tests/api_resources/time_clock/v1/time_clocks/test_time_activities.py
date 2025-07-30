# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from connecteam_api_sdk import ConnecteamAPISDK, AsyncConnecteamAPISDK
from connecteam_api_sdk.types.time_clock.v1.time_clocks import (
    TimeActivityListResponse,
    TimeActivityCreateResponse,
    TimeActivityUpdateResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTimeActivities:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: ConnecteamAPISDK) -> None:
        time_activity = client.time_clock.v1.time_clocks.time_activities.create(
            time_clock_id=0,
            time_activities=[
                {
                    "shifts": [
                        {
                            "job_id": "jobId",
                            "start": {
                                "timestamp": 1,
                                "timezone": "timezone",
                            },
                        }
                    ],
                    "user_id": 1,
                }
            ],
        )
        assert_matches_type(TimeActivityCreateResponse, time_activity, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: ConnecteamAPISDK) -> None:
        response = client.time_clock.v1.time_clocks.time_activities.with_raw_response.create(
            time_clock_id=0,
            time_activities=[
                {
                    "shifts": [
                        {
                            "job_id": "jobId",
                            "start": {
                                "timestamp": 1,
                                "timezone": "timezone",
                            },
                        }
                    ],
                    "user_id": 1,
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        time_activity = response.parse()
        assert_matches_type(TimeActivityCreateResponse, time_activity, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: ConnecteamAPISDK) -> None:
        with client.time_clock.v1.time_clocks.time_activities.with_streaming_response.create(
            time_clock_id=0,
            time_activities=[
                {
                    "shifts": [
                        {
                            "job_id": "jobId",
                            "start": {
                                "timestamp": 1,
                                "timezone": "timezone",
                            },
                        }
                    ],
                    "user_id": 1,
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            time_activity = response.parse()
            assert_matches_type(TimeActivityCreateResponse, time_activity, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: ConnecteamAPISDK) -> None:
        time_activity = client.time_clock.v1.time_clocks.time_activities.update(
            time_clock_id=0,
            time_activities=[
                {
                    "shifts": [{"id": "id"}],
                    "user_id": 1,
                }
            ],
        )
        assert_matches_type(TimeActivityUpdateResponse, time_activity, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: ConnecteamAPISDK) -> None:
        response = client.time_clock.v1.time_clocks.time_activities.with_raw_response.update(
            time_clock_id=0,
            time_activities=[
                {
                    "shifts": [{"id": "id"}],
                    "user_id": 1,
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        time_activity = response.parse()
        assert_matches_type(TimeActivityUpdateResponse, time_activity, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: ConnecteamAPISDK) -> None:
        with client.time_clock.v1.time_clocks.time_activities.with_streaming_response.update(
            time_clock_id=0,
            time_activities=[
                {
                    "shifts": [{"id": "id"}],
                    "user_id": 1,
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            time_activity = response.parse()
            assert_matches_type(TimeActivityUpdateResponse, time_activity, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: ConnecteamAPISDK) -> None:
        time_activity = client.time_clock.v1.time_clocks.time_activities.list(
            time_clock_id=0,
            end_date="endDate",
            start_date="startDate",
        )
        assert_matches_type(TimeActivityListResponse, time_activity, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: ConnecteamAPISDK) -> None:
        time_activity = client.time_clock.v1.time_clocks.time_activities.list(
            time_clock_id=0,
            end_date="endDate",
            start_date="startDate",
            activity_types=["shift"],
            job_ids=["string"],
            manual_break_ids=["string"],
            policy_type_ids=["string"],
            user_ids=[1],
        )
        assert_matches_type(TimeActivityListResponse, time_activity, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: ConnecteamAPISDK) -> None:
        response = client.time_clock.v1.time_clocks.time_activities.with_raw_response.list(
            time_clock_id=0,
            end_date="endDate",
            start_date="startDate",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        time_activity = response.parse()
        assert_matches_type(TimeActivityListResponse, time_activity, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: ConnecteamAPISDK) -> None:
        with client.time_clock.v1.time_clocks.time_activities.with_streaming_response.list(
            time_clock_id=0,
            end_date="endDate",
            start_date="startDate",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            time_activity = response.parse()
            assert_matches_type(TimeActivityListResponse, time_activity, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncTimeActivities:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncConnecteamAPISDK) -> None:
        time_activity = await async_client.time_clock.v1.time_clocks.time_activities.create(
            time_clock_id=0,
            time_activities=[
                {
                    "shifts": [
                        {
                            "job_id": "jobId",
                            "start": {
                                "timestamp": 1,
                                "timezone": "timezone",
                            },
                        }
                    ],
                    "user_id": 1,
                }
            ],
        )
        assert_matches_type(TimeActivityCreateResponse, time_activity, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.time_clock.v1.time_clocks.time_activities.with_raw_response.create(
            time_clock_id=0,
            time_activities=[
                {
                    "shifts": [
                        {
                            "job_id": "jobId",
                            "start": {
                                "timestamp": 1,
                                "timezone": "timezone",
                            },
                        }
                    ],
                    "user_id": 1,
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        time_activity = await response.parse()
        assert_matches_type(TimeActivityCreateResponse, time_activity, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.time_clock.v1.time_clocks.time_activities.with_streaming_response.create(
            time_clock_id=0,
            time_activities=[
                {
                    "shifts": [
                        {
                            "job_id": "jobId",
                            "start": {
                                "timestamp": 1,
                                "timezone": "timezone",
                            },
                        }
                    ],
                    "user_id": 1,
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            time_activity = await response.parse()
            assert_matches_type(TimeActivityCreateResponse, time_activity, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        time_activity = await async_client.time_clock.v1.time_clocks.time_activities.update(
            time_clock_id=0,
            time_activities=[
                {
                    "shifts": [{"id": "id"}],
                    "user_id": 1,
                }
            ],
        )
        assert_matches_type(TimeActivityUpdateResponse, time_activity, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.time_clock.v1.time_clocks.time_activities.with_raw_response.update(
            time_clock_id=0,
            time_activities=[
                {
                    "shifts": [{"id": "id"}],
                    "user_id": 1,
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        time_activity = await response.parse()
        assert_matches_type(TimeActivityUpdateResponse, time_activity, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.time_clock.v1.time_clocks.time_activities.with_streaming_response.update(
            time_clock_id=0,
            time_activities=[
                {
                    "shifts": [{"id": "id"}],
                    "user_id": 1,
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            time_activity = await response.parse()
            assert_matches_type(TimeActivityUpdateResponse, time_activity, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        time_activity = await async_client.time_clock.v1.time_clocks.time_activities.list(
            time_clock_id=0,
            end_date="endDate",
            start_date="startDate",
        )
        assert_matches_type(TimeActivityListResponse, time_activity, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        time_activity = await async_client.time_clock.v1.time_clocks.time_activities.list(
            time_clock_id=0,
            end_date="endDate",
            start_date="startDate",
            activity_types=["shift"],
            job_ids=["string"],
            manual_break_ids=["string"],
            policy_type_ids=["string"],
            user_ids=[1],
        )
        assert_matches_type(TimeActivityListResponse, time_activity, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.time_clock.v1.time_clocks.time_activities.with_raw_response.list(
            time_clock_id=0,
            end_date="endDate",
            start_date="startDate",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        time_activity = await response.parse()
        assert_matches_type(TimeActivityListResponse, time_activity, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.time_clock.v1.time_clocks.time_activities.with_streaming_response.list(
            time_clock_id=0,
            end_date="endDate",
            start_date="startDate",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            time_activity = await response.parse()
            assert_matches_type(TimeActivityListResponse, time_activity, path=["response"])

        assert cast(Any, response.is_closed) is True
