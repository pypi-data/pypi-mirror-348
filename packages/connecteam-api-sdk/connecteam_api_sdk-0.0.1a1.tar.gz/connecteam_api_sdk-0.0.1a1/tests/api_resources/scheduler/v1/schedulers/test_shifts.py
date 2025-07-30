# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from connecteam_api_sdk import ConnecteamAPISDK, AsyncConnecteamAPISDK
from connecteam_api_sdk.types.scheduler.v1.schedulers import (
    ShiftListResponse,
    ShiftDeleteResponse,
    APIResponseShiftBulk,
    ShiftRetrieveResponse,
    ShiftDeleteShiftResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestShifts:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: ConnecteamAPISDK) -> None:
        shift = client.scheduler.v1.schedulers.shifts.create(
            scheduler_id=0,
            body=[
                {
                    "end_time": 1,
                    "start_time": 1,
                }
            ],
        )
        assert_matches_type(APIResponseShiftBulk, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: ConnecteamAPISDK) -> None:
        shift = client.scheduler.v1.schedulers.shifts.create(
            scheduler_id=0,
            body=[
                {
                    "end_time": 1,
                    "start_time": 1,
                    "assigned_user_ids": [1],
                    "breaks": [
                        {
                            "duration": 0,
                            "name": "name",
                            "type": "paid",
                            "start_time": 0,
                        }
                    ],
                    "color": "color",
                    "is_open_shift": True,
                    "is_published": True,
                    "is_require_admin_approval": True,
                    "job_id": "jobId",
                    "location_data": {
                        "is_referenced_to_job": True,
                        "gps": {
                            "address": "address",
                            "latitude": 0,
                            "longitude": 0,
                        },
                    },
                    "notes": [{"html": "html"}],
                    "shift_details": {
                        "shift_layers": [
                            {
                                "id": "id",
                                "value": {"id": "id"},
                            }
                        ],
                        "shift_source": "shiftSource",
                    },
                    "statuses": [
                        {
                            "gps": {
                                "address": "address",
                                "latitude": 0,
                                "longitude": 0,
                            },
                            "note": "note",
                            "should_override_previous_statuses": True,
                        }
                    ],
                    "timezone": "timezone",
                    "title": "title",
                }
            ],
            notify_users=True,
        )
        assert_matches_type(APIResponseShiftBulk, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: ConnecteamAPISDK) -> None:
        response = client.scheduler.v1.schedulers.shifts.with_raw_response.create(
            scheduler_id=0,
            body=[
                {
                    "end_time": 1,
                    "start_time": 1,
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        shift = response.parse()
        assert_matches_type(APIResponseShiftBulk, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: ConnecteamAPISDK) -> None:
        with client.scheduler.v1.schedulers.shifts.with_streaming_response.create(
            scheduler_id=0,
            body=[
                {
                    "end_time": 1,
                    "start_time": 1,
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            shift = response.parse()
            assert_matches_type(APIResponseShiftBulk, shift, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: ConnecteamAPISDK) -> None:
        shift = client.scheduler.v1.schedulers.shifts.retrieve(
            shift_id="shiftId",
            scheduler_id=0,
        )
        assert_matches_type(ShiftRetrieveResponse, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: ConnecteamAPISDK) -> None:
        response = client.scheduler.v1.schedulers.shifts.with_raw_response.retrieve(
            shift_id="shiftId",
            scheduler_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        shift = response.parse()
        assert_matches_type(ShiftRetrieveResponse, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: ConnecteamAPISDK) -> None:
        with client.scheduler.v1.schedulers.shifts.with_streaming_response.retrieve(
            shift_id="shiftId",
            scheduler_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            shift = response.parse()
            assert_matches_type(ShiftRetrieveResponse, shift, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: ConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `shift_id` but received ''"):
            client.scheduler.v1.schedulers.shifts.with_raw_response.retrieve(
                shift_id="",
                scheduler_id=0,
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: ConnecteamAPISDK) -> None:
        shift = client.scheduler.v1.schedulers.shifts.update(
            scheduler_id=0,
            body=[{"shift_id": "shiftId"}],
        )
        assert_matches_type(APIResponseShiftBulk, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: ConnecteamAPISDK) -> None:
        shift = client.scheduler.v1.schedulers.shifts.update(
            scheduler_id=0,
            body=[
                {
                    "shift_id": "shiftId",
                    "assigned_user_ids": [1],
                    "breaks": [
                        {
                            "duration": 0,
                            "name": "name",
                            "type": "paid",
                            "id": "id",
                            "start_time": 0,
                        }
                    ],
                    "color": "color",
                    "end_time": 1,
                    "is_edit_for_all_users": True,
                    "is_open_shift": True,
                    "is_published": True,
                    "is_require_admin_approval": True,
                    "job_id": "jobId",
                    "location_data": {
                        "is_referenced_to_job": True,
                        "gps": {
                            "address": "address",
                            "latitude": 0,
                            "longitude": 0,
                        },
                    },
                    "notes": [{"html": "html"}],
                    "start_time": 1,
                    "timezone": "timezone",
                    "title": "title",
                }
            ],
            notify_users=True,
        )
        assert_matches_type(APIResponseShiftBulk, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: ConnecteamAPISDK) -> None:
        response = client.scheduler.v1.schedulers.shifts.with_raw_response.update(
            scheduler_id=0,
            body=[{"shift_id": "shiftId"}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        shift = response.parse()
        assert_matches_type(APIResponseShiftBulk, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: ConnecteamAPISDK) -> None:
        with client.scheduler.v1.schedulers.shifts.with_streaming_response.update(
            scheduler_id=0,
            body=[{"shift_id": "shiftId"}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            shift = response.parse()
            assert_matches_type(APIResponseShiftBulk, shift, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: ConnecteamAPISDK) -> None:
        shift = client.scheduler.v1.schedulers.shifts.list(
            scheduler_id=0,
            end_time=1,
            start_time=1,
        )
        assert_matches_type(ShiftListResponse, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: ConnecteamAPISDK) -> None:
        shift = client.scheduler.v1.schedulers.shifts.list(
            scheduler_id=0,
            end_time=1,
            start_time=1,
            assigned_user_ids=[1],
            is_open_shift=True,
            is_published=True,
            is_require_admin_approval=True,
            job_id=["string"],
            limit=1,
            offset=0,
            order="asc",
            shift_id=["string"],
            sort="created_at",
            title="title",
        )
        assert_matches_type(ShiftListResponse, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: ConnecteamAPISDK) -> None:
        response = client.scheduler.v1.schedulers.shifts.with_raw_response.list(
            scheduler_id=0,
            end_time=1,
            start_time=1,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        shift = response.parse()
        assert_matches_type(ShiftListResponse, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: ConnecteamAPISDK) -> None:
        with client.scheduler.v1.schedulers.shifts.with_streaming_response.list(
            scheduler_id=0,
            end_time=1,
            start_time=1,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            shift = response.parse()
            assert_matches_type(ShiftListResponse, shift, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: ConnecteamAPISDK) -> None:
        shift = client.scheduler.v1.schedulers.shifts.delete(
            scheduler_id=0,
            shifts_ids=["string"],
        )
        assert_matches_type(ShiftDeleteResponse, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_delete_with_all_params(self, client: ConnecteamAPISDK) -> None:
        shift = client.scheduler.v1.schedulers.shifts.delete(
            scheduler_id=0,
            shifts_ids=["string"],
            notify_users=True,
        )
        assert_matches_type(ShiftDeleteResponse, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: ConnecteamAPISDK) -> None:
        response = client.scheduler.v1.schedulers.shifts.with_raw_response.delete(
            scheduler_id=0,
            shifts_ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        shift = response.parse()
        assert_matches_type(ShiftDeleteResponse, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: ConnecteamAPISDK) -> None:
        with client.scheduler.v1.schedulers.shifts.with_streaming_response.delete(
            scheduler_id=0,
            shifts_ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            shift = response.parse()
            assert_matches_type(ShiftDeleteResponse, shift, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete_shift(self, client: ConnecteamAPISDK) -> None:
        shift = client.scheduler.v1.schedulers.shifts.delete_shift(
            shift_id="shiftId",
            scheduler_id=0,
        )
        assert_matches_type(ShiftDeleteShiftResponse, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_delete_shift_with_all_params(self, client: ConnecteamAPISDK) -> None:
        shift = client.scheduler.v1.schedulers.shifts.delete_shift(
            shift_id="shiftId",
            scheduler_id=0,
            notify_users=True,
        )
        assert_matches_type(ShiftDeleteShiftResponse, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete_shift(self, client: ConnecteamAPISDK) -> None:
        response = client.scheduler.v1.schedulers.shifts.with_raw_response.delete_shift(
            shift_id="shiftId",
            scheduler_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        shift = response.parse()
        assert_matches_type(ShiftDeleteShiftResponse, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete_shift(self, client: ConnecteamAPISDK) -> None:
        with client.scheduler.v1.schedulers.shifts.with_streaming_response.delete_shift(
            shift_id="shiftId",
            scheduler_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            shift = response.parse()
            assert_matches_type(ShiftDeleteShiftResponse, shift, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete_shift(self, client: ConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `shift_id` but received ''"):
            client.scheduler.v1.schedulers.shifts.with_raw_response.delete_shift(
                shift_id="",
                scheduler_id=0,
            )


class TestAsyncShifts:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncConnecteamAPISDK) -> None:
        shift = await async_client.scheduler.v1.schedulers.shifts.create(
            scheduler_id=0,
            body=[
                {
                    "end_time": 1,
                    "start_time": 1,
                }
            ],
        )
        assert_matches_type(APIResponseShiftBulk, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        shift = await async_client.scheduler.v1.schedulers.shifts.create(
            scheduler_id=0,
            body=[
                {
                    "end_time": 1,
                    "start_time": 1,
                    "assigned_user_ids": [1],
                    "breaks": [
                        {
                            "duration": 0,
                            "name": "name",
                            "type": "paid",
                            "start_time": 0,
                        }
                    ],
                    "color": "color",
                    "is_open_shift": True,
                    "is_published": True,
                    "is_require_admin_approval": True,
                    "job_id": "jobId",
                    "location_data": {
                        "is_referenced_to_job": True,
                        "gps": {
                            "address": "address",
                            "latitude": 0,
                            "longitude": 0,
                        },
                    },
                    "notes": [{"html": "html"}],
                    "shift_details": {
                        "shift_layers": [
                            {
                                "id": "id",
                                "value": {"id": "id"},
                            }
                        ],
                        "shift_source": "shiftSource",
                    },
                    "statuses": [
                        {
                            "gps": {
                                "address": "address",
                                "latitude": 0,
                                "longitude": 0,
                            },
                            "note": "note",
                            "should_override_previous_statuses": True,
                        }
                    ],
                    "timezone": "timezone",
                    "title": "title",
                }
            ],
            notify_users=True,
        )
        assert_matches_type(APIResponseShiftBulk, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.scheduler.v1.schedulers.shifts.with_raw_response.create(
            scheduler_id=0,
            body=[
                {
                    "end_time": 1,
                    "start_time": 1,
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        shift = await response.parse()
        assert_matches_type(APIResponseShiftBulk, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.scheduler.v1.schedulers.shifts.with_streaming_response.create(
            scheduler_id=0,
            body=[
                {
                    "end_time": 1,
                    "start_time": 1,
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            shift = await response.parse()
            assert_matches_type(APIResponseShiftBulk, shift, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncConnecteamAPISDK) -> None:
        shift = await async_client.scheduler.v1.schedulers.shifts.retrieve(
            shift_id="shiftId",
            scheduler_id=0,
        )
        assert_matches_type(ShiftRetrieveResponse, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.scheduler.v1.schedulers.shifts.with_raw_response.retrieve(
            shift_id="shiftId",
            scheduler_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        shift = await response.parse()
        assert_matches_type(ShiftRetrieveResponse, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.scheduler.v1.schedulers.shifts.with_streaming_response.retrieve(
            shift_id="shiftId",
            scheduler_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            shift = await response.parse()
            assert_matches_type(ShiftRetrieveResponse, shift, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `shift_id` but received ''"):
            await async_client.scheduler.v1.schedulers.shifts.with_raw_response.retrieve(
                shift_id="",
                scheduler_id=0,
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        shift = await async_client.scheduler.v1.schedulers.shifts.update(
            scheduler_id=0,
            body=[{"shift_id": "shiftId"}],
        )
        assert_matches_type(APIResponseShiftBulk, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        shift = await async_client.scheduler.v1.schedulers.shifts.update(
            scheduler_id=0,
            body=[
                {
                    "shift_id": "shiftId",
                    "assigned_user_ids": [1],
                    "breaks": [
                        {
                            "duration": 0,
                            "name": "name",
                            "type": "paid",
                            "id": "id",
                            "start_time": 0,
                        }
                    ],
                    "color": "color",
                    "end_time": 1,
                    "is_edit_for_all_users": True,
                    "is_open_shift": True,
                    "is_published": True,
                    "is_require_admin_approval": True,
                    "job_id": "jobId",
                    "location_data": {
                        "is_referenced_to_job": True,
                        "gps": {
                            "address": "address",
                            "latitude": 0,
                            "longitude": 0,
                        },
                    },
                    "notes": [{"html": "html"}],
                    "start_time": 1,
                    "timezone": "timezone",
                    "title": "title",
                }
            ],
            notify_users=True,
        )
        assert_matches_type(APIResponseShiftBulk, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.scheduler.v1.schedulers.shifts.with_raw_response.update(
            scheduler_id=0,
            body=[{"shift_id": "shiftId"}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        shift = await response.parse()
        assert_matches_type(APIResponseShiftBulk, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.scheduler.v1.schedulers.shifts.with_streaming_response.update(
            scheduler_id=0,
            body=[{"shift_id": "shiftId"}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            shift = await response.parse()
            assert_matches_type(APIResponseShiftBulk, shift, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        shift = await async_client.scheduler.v1.schedulers.shifts.list(
            scheduler_id=0,
            end_time=1,
            start_time=1,
        )
        assert_matches_type(ShiftListResponse, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        shift = await async_client.scheduler.v1.schedulers.shifts.list(
            scheduler_id=0,
            end_time=1,
            start_time=1,
            assigned_user_ids=[1],
            is_open_shift=True,
            is_published=True,
            is_require_admin_approval=True,
            job_id=["string"],
            limit=1,
            offset=0,
            order="asc",
            shift_id=["string"],
            sort="created_at",
            title="title",
        )
        assert_matches_type(ShiftListResponse, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.scheduler.v1.schedulers.shifts.with_raw_response.list(
            scheduler_id=0,
            end_time=1,
            start_time=1,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        shift = await response.parse()
        assert_matches_type(ShiftListResponse, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.scheduler.v1.schedulers.shifts.with_streaming_response.list(
            scheduler_id=0,
            end_time=1,
            start_time=1,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            shift = await response.parse()
            assert_matches_type(ShiftListResponse, shift, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncConnecteamAPISDK) -> None:
        shift = await async_client.scheduler.v1.schedulers.shifts.delete(
            scheduler_id=0,
            shifts_ids=["string"],
        )
        assert_matches_type(ShiftDeleteResponse, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        shift = await async_client.scheduler.v1.schedulers.shifts.delete(
            scheduler_id=0,
            shifts_ids=["string"],
            notify_users=True,
        )
        assert_matches_type(ShiftDeleteResponse, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.scheduler.v1.schedulers.shifts.with_raw_response.delete(
            scheduler_id=0,
            shifts_ids=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        shift = await response.parse()
        assert_matches_type(ShiftDeleteResponse, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.scheduler.v1.schedulers.shifts.with_streaming_response.delete(
            scheduler_id=0,
            shifts_ids=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            shift = await response.parse()
            assert_matches_type(ShiftDeleteResponse, shift, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete_shift(self, async_client: AsyncConnecteamAPISDK) -> None:
        shift = await async_client.scheduler.v1.schedulers.shifts.delete_shift(
            shift_id="shiftId",
            scheduler_id=0,
        )
        assert_matches_type(ShiftDeleteShiftResponse, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete_shift_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        shift = await async_client.scheduler.v1.schedulers.shifts.delete_shift(
            shift_id="shiftId",
            scheduler_id=0,
            notify_users=True,
        )
        assert_matches_type(ShiftDeleteShiftResponse, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete_shift(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.scheduler.v1.schedulers.shifts.with_raw_response.delete_shift(
            shift_id="shiftId",
            scheduler_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        shift = await response.parse()
        assert_matches_type(ShiftDeleteShiftResponse, shift, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete_shift(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.scheduler.v1.schedulers.shifts.with_streaming_response.delete_shift(
            shift_id="shiftId",
            scheduler_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            shift = await response.parse()
            assert_matches_type(ShiftDeleteShiftResponse, shift, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete_shift(self, async_client: AsyncConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `shift_id` but received ''"):
            await async_client.scheduler.v1.schedulers.shifts.with_raw_response.delete_shift(
                shift_id="",
                scheduler_id=0,
            )
