# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from connecteam_api_sdk import ConnecteamAPISDK, AsyncConnecteamAPISDK
from connecteam_api_sdk._utils import parse_date
from connecteam_api_sdk.types.users.v1 import (
    UserListResponse,
    UserCreateResponse,
    UserUpdateResponse,
    UserArchiveResponse,
    UserCreateNoteResponse,
    UserUpdatePerformanceResponse,
)
from connecteam_api_sdk.types.users.v1.custom_fields import APIResponseBase

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUsers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: ConnecteamAPISDK) -> None:
        user = client.users.v1.users.create(
            body=[
                {
                    "first_name": "firstName",
                    "last_name": "lastName",
                    "phone_number": "phoneNumber",
                    "user_type": "user",
                }
            ],
        )
        assert_matches_type(UserCreateResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: ConnecteamAPISDK) -> None:
        user = client.users.v1.users.create(
            body=[
                {
                    "first_name": "firstName",
                    "last_name": "lastName",
                    "phone_number": "phoneNumber",
                    "user_type": "user",
                    "custom_fields": [
                        {
                            "custom_field_id": 1,
                            "value": {},
                        }
                    ],
                    "email": "email",
                    "is_archived": True,
                }
            ],
            send_activation=True,
        )
        assert_matches_type(UserCreateResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: ConnecteamAPISDK) -> None:
        response = client.users.v1.users.with_raw_response.create(
            body=[
                {
                    "first_name": "firstName",
                    "last_name": "lastName",
                    "phone_number": "phoneNumber",
                    "user_type": "user",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(UserCreateResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: ConnecteamAPISDK) -> None:
        with client.users.v1.users.with_streaming_response.create(
            body=[
                {
                    "first_name": "firstName",
                    "last_name": "lastName",
                    "phone_number": "phoneNumber",
                    "user_type": "user",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(UserCreateResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: ConnecteamAPISDK) -> None:
        user = client.users.v1.users.update(
            body=[{}],
        )
        assert_matches_type(UserUpdateResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: ConnecteamAPISDK) -> None:
        user = client.users.v1.users.update(
            body=[
                {
                    "custom_fields": [
                        {
                            "custom_field_id": 1,
                            "value": {},
                        }
                    ],
                    "email": "email",
                    "first_name": "firstName",
                    "is_archived": True,
                    "last_name": "lastName",
                    "phone_number": "phoneNumber",
                    "user_id": 1,
                    "user_type": "user",
                }
            ],
            edit_users_by_phone=True,
            include_smart_group_ids=True,
        )
        assert_matches_type(UserUpdateResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: ConnecteamAPISDK) -> None:
        response = client.users.v1.users.with_raw_response.update(
            body=[{}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(UserUpdateResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: ConnecteamAPISDK) -> None:
        with client.users.v1.users.with_streaming_response.update(
            body=[{}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(UserUpdateResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: ConnecteamAPISDK) -> None:
        user = client.users.v1.users.list()
        assert_matches_type(UserListResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: ConnecteamAPISDK) -> None:
        user = client.users.v1.users.list(
            created_at=1,
            email_addresses=["string"],
            full_names=["string"],
            limit=1,
            modified_at=1,
            offset=0,
            order="asc",
            phone_numbers=["string"],
            sort="created_at",
            user_ids=[1],
            user_status="active",
        )
        assert_matches_type(UserListResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: ConnecteamAPISDK) -> None:
        response = client.users.v1.users.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(UserListResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: ConnecteamAPISDK) -> None:
        with client.users.v1.users.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(UserListResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_archive(self, client: ConnecteamAPISDK) -> None:
        user = client.users.v1.users.archive(
            body=[1],
        )
        assert_matches_type(UserArchiveResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_archive(self, client: ConnecteamAPISDK) -> None:
        response = client.users.v1.users.with_raw_response.archive(
            body=[1],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(UserArchiveResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_archive(self, client: ConnecteamAPISDK) -> None:
        with client.users.v1.users.with_streaming_response.archive(
            body=[1],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(UserArchiveResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_create_note(self, client: ConnecteamAPISDK) -> None:
        user = client.users.v1.users.create_note(
            user_id=0,
            text="x",
        )
        assert_matches_type(UserCreateNoteResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_note_with_all_params(self, client: ConnecteamAPISDK) -> None:
        user = client.users.v1.users.create_note(
            user_id=0,
            text="x",
            title="title",
        )
        assert_matches_type(UserCreateNoteResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_note(self, client: ConnecteamAPISDK) -> None:
        response = client.users.v1.users.with_raw_response.create_note(
            user_id=0,
            text="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(UserCreateNoteResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_note(self, client: ConnecteamAPISDK) -> None:
        with client.users.v1.users.with_streaming_response.create_note(
            user_id=0,
            text="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(UserCreateNoteResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_update_performance(self, client: ConnecteamAPISDK) -> None:
        user = client.users.v1.users.update_performance(
            date=parse_date("2019-12-27"),
            user_id=1,
            items=[
                {
                    "indicator_id": 1,
                    "value": 0,
                }
            ],
        )
        assert_matches_type(UserUpdatePerformanceResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update_performance(self, client: ConnecteamAPISDK) -> None:
        response = client.users.v1.users.with_raw_response.update_performance(
            date=parse_date("2019-12-27"),
            user_id=1,
            items=[
                {
                    "indicator_id": 1,
                    "value": 0,
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(UserUpdatePerformanceResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update_performance(self, client: ConnecteamAPISDK) -> None:
        with client.users.v1.users.with_streaming_response.update_performance(
            date=parse_date("2019-12-27"),
            user_id=1,
            items=[
                {
                    "indicator_id": 1,
                    "value": 0,
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(UserUpdatePerformanceResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update_performance(self, client: ConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `date` but received ''"):
            client.users.v1.users.with_raw_response.update_performance(
                date="",
                user_id=1,
                items=[
                    {
                        "indicator_id": 1,
                        "value": 0,
                    }
                ],
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_upload_payslip(self, client: ConnecteamAPISDK) -> None:
        user = client.users.v1.users.upload_payslip(
            user_id=0,
            end_date="endDate",
            file_id="fileId",
            start_date="startDate",
        )
        assert_matches_type(APIResponseBase, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_upload_payslip(self, client: ConnecteamAPISDK) -> None:
        response = client.users.v1.users.with_raw_response.upload_payslip(
            user_id=0,
            end_date="endDate",
            file_id="fileId",
            start_date="startDate",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = response.parse()
        assert_matches_type(APIResponseBase, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_upload_payslip(self, client: ConnecteamAPISDK) -> None:
        with client.users.v1.users.with_streaming_response.upload_payslip(
            user_id=0,
            end_date="endDate",
            file_id="fileId",
            start_date="startDate",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = response.parse()
            assert_matches_type(APIResponseBase, user, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncUsers:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncConnecteamAPISDK) -> None:
        user = await async_client.users.v1.users.create(
            body=[
                {
                    "first_name": "firstName",
                    "last_name": "lastName",
                    "phone_number": "phoneNumber",
                    "user_type": "user",
                }
            ],
        )
        assert_matches_type(UserCreateResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        user = await async_client.users.v1.users.create(
            body=[
                {
                    "first_name": "firstName",
                    "last_name": "lastName",
                    "phone_number": "phoneNumber",
                    "user_type": "user",
                    "custom_fields": [
                        {
                            "custom_field_id": 1,
                            "value": {},
                        }
                    ],
                    "email": "email",
                    "is_archived": True,
                }
            ],
            send_activation=True,
        )
        assert_matches_type(UserCreateResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.users.v1.users.with_raw_response.create(
            body=[
                {
                    "first_name": "firstName",
                    "last_name": "lastName",
                    "phone_number": "phoneNumber",
                    "user_type": "user",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(UserCreateResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.users.v1.users.with_streaming_response.create(
            body=[
                {
                    "first_name": "firstName",
                    "last_name": "lastName",
                    "phone_number": "phoneNumber",
                    "user_type": "user",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(UserCreateResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        user = await async_client.users.v1.users.update(
            body=[{}],
        )
        assert_matches_type(UserUpdateResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        user = await async_client.users.v1.users.update(
            body=[
                {
                    "custom_fields": [
                        {
                            "custom_field_id": 1,
                            "value": {},
                        }
                    ],
                    "email": "email",
                    "first_name": "firstName",
                    "is_archived": True,
                    "last_name": "lastName",
                    "phone_number": "phoneNumber",
                    "user_id": 1,
                    "user_type": "user",
                }
            ],
            edit_users_by_phone=True,
            include_smart_group_ids=True,
        )
        assert_matches_type(UserUpdateResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.users.v1.users.with_raw_response.update(
            body=[{}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(UserUpdateResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.users.v1.users.with_streaming_response.update(
            body=[{}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(UserUpdateResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        user = await async_client.users.v1.users.list()
        assert_matches_type(UserListResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        user = await async_client.users.v1.users.list(
            created_at=1,
            email_addresses=["string"],
            full_names=["string"],
            limit=1,
            modified_at=1,
            offset=0,
            order="asc",
            phone_numbers=["string"],
            sort="created_at",
            user_ids=[1],
            user_status="active",
        )
        assert_matches_type(UserListResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.users.v1.users.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(UserListResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.users.v1.users.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(UserListResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_archive(self, async_client: AsyncConnecteamAPISDK) -> None:
        user = await async_client.users.v1.users.archive(
            body=[1],
        )
        assert_matches_type(UserArchiveResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_archive(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.users.v1.users.with_raw_response.archive(
            body=[1],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(UserArchiveResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_archive(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.users.v1.users.with_streaming_response.archive(
            body=[1],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(UserArchiveResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_note(self, async_client: AsyncConnecteamAPISDK) -> None:
        user = await async_client.users.v1.users.create_note(
            user_id=0,
            text="x",
        )
        assert_matches_type(UserCreateNoteResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_note_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        user = await async_client.users.v1.users.create_note(
            user_id=0,
            text="x",
            title="title",
        )
        assert_matches_type(UserCreateNoteResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_note(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.users.v1.users.with_raw_response.create_note(
            user_id=0,
            text="x",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(UserCreateNoteResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_note(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.users.v1.users.with_streaming_response.create_note(
            user_id=0,
            text="x",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(UserCreateNoteResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_performance(self, async_client: AsyncConnecteamAPISDK) -> None:
        user = await async_client.users.v1.users.update_performance(
            date=parse_date("2019-12-27"),
            user_id=1,
            items=[
                {
                    "indicator_id": 1,
                    "value": 0,
                }
            ],
        )
        assert_matches_type(UserUpdatePerformanceResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update_performance(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.users.v1.users.with_raw_response.update_performance(
            date=parse_date("2019-12-27"),
            user_id=1,
            items=[
                {
                    "indicator_id": 1,
                    "value": 0,
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(UserUpdatePerformanceResponse, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update_performance(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.users.v1.users.with_streaming_response.update_performance(
            date=parse_date("2019-12-27"),
            user_id=1,
            items=[
                {
                    "indicator_id": 1,
                    "value": 0,
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(UserUpdatePerformanceResponse, user, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update_performance(self, async_client: AsyncConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `date` but received ''"):
            await async_client.users.v1.users.with_raw_response.update_performance(
                date="",
                user_id=1,
                items=[
                    {
                        "indicator_id": 1,
                        "value": 0,
                    }
                ],
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_upload_payslip(self, async_client: AsyncConnecteamAPISDK) -> None:
        user = await async_client.users.v1.users.upload_payslip(
            user_id=0,
            end_date="endDate",
            file_id="fileId",
            start_date="startDate",
        )
        assert_matches_type(APIResponseBase, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_upload_payslip(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.users.v1.users.with_raw_response.upload_payslip(
            user_id=0,
            end_date="endDate",
            file_id="fileId",
            start_date="startDate",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        user = await response.parse()
        assert_matches_type(APIResponseBase, user, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_upload_payslip(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.users.v1.users.with_streaming_response.upload_payslip(
            user_id=0,
            end_date="endDate",
            file_id="fileId",
            start_date="startDate",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            user = await response.parse()
            assert_matches_type(APIResponseBase, user, path=["response"])

        assert cast(Any, response.is_closed) is True
