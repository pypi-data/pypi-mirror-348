# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from connecteam_api_sdk import ConnecteamAPISDK, AsyncConnecteamAPISDK
from connecteam_api_sdk.types.users.v1 import (
    CustomFieldListResponse,
    CustomFieldDeleteResponse,
    APIResponseGetCustomFieldsSettings,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCustomFields:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: ConnecteamAPISDK) -> None:
        custom_field = client.users.v1.custom_fields.create(
            custom_fields=[
                {
                    "category_id": 0,
                    "is_editable_for_all_admins": True,
                    "is_editable_for_users": True,
                    "is_multi_select": True,
                    "is_required": True,
                    "is_visible_to_all_admins": True,
                    "is_visible_to_users": True,
                    "name": "name",
                }
            ],
        )
        assert_matches_type(APIResponseGetCustomFieldsSettings, custom_field, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: ConnecteamAPISDK) -> None:
        response = client.users.v1.custom_fields.with_raw_response.create(
            custom_fields=[
                {
                    "category_id": 0,
                    "is_editable_for_all_admins": True,
                    "is_editable_for_users": True,
                    "is_multi_select": True,
                    "is_required": True,
                    "is_visible_to_all_admins": True,
                    "is_visible_to_users": True,
                    "name": "name",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        custom_field = response.parse()
        assert_matches_type(APIResponseGetCustomFieldsSettings, custom_field, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: ConnecteamAPISDK) -> None:
        with client.users.v1.custom_fields.with_streaming_response.create(
            custom_fields=[
                {
                    "category_id": 0,
                    "is_editable_for_all_admins": True,
                    "is_editable_for_users": True,
                    "is_multi_select": True,
                    "is_required": True,
                    "is_visible_to_all_admins": True,
                    "is_visible_to_users": True,
                    "name": "name",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            custom_field = response.parse()
            assert_matches_type(APIResponseGetCustomFieldsSettings, custom_field, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: ConnecteamAPISDK) -> None:
        custom_field = client.users.v1.custom_fields.update(
            custom_fields=[{"id": 0}],
        )
        assert_matches_type(APIResponseGetCustomFieldsSettings, custom_field, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: ConnecteamAPISDK) -> None:
        response = client.users.v1.custom_fields.with_raw_response.update(
            custom_fields=[{"id": 0}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        custom_field = response.parse()
        assert_matches_type(APIResponseGetCustomFieldsSettings, custom_field, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: ConnecteamAPISDK) -> None:
        with client.users.v1.custom_fields.with_streaming_response.update(
            custom_fields=[{"id": 0}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            custom_field = response.parse()
            assert_matches_type(APIResponseGetCustomFieldsSettings, custom_field, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: ConnecteamAPISDK) -> None:
        custom_field = client.users.v1.custom_fields.list()
        assert_matches_type(CustomFieldListResponse, custom_field, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: ConnecteamAPISDK) -> None:
        custom_field = client.users.v1.custom_fields.list(
            category_ids=[0],
            custom_field_ids=[0],
            custom_field_names=["string"],
            custom_field_types=["email"],
            limit=1,
            offset=0,
            order="asc",
            sort="id",
        )
        assert_matches_type(CustomFieldListResponse, custom_field, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: ConnecteamAPISDK) -> None:
        response = client.users.v1.custom_fields.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        custom_field = response.parse()
        assert_matches_type(CustomFieldListResponse, custom_field, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: ConnecteamAPISDK) -> None:
        with client.users.v1.custom_fields.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            custom_field = response.parse()
            assert_matches_type(CustomFieldListResponse, custom_field, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: ConnecteamAPISDK) -> None:
        custom_field = client.users.v1.custom_fields.delete(
            custom_field_ids=[0],
        )
        assert_matches_type(CustomFieldDeleteResponse, custom_field, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: ConnecteamAPISDK) -> None:
        response = client.users.v1.custom_fields.with_raw_response.delete(
            custom_field_ids=[0],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        custom_field = response.parse()
        assert_matches_type(CustomFieldDeleteResponse, custom_field, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: ConnecteamAPISDK) -> None:
        with client.users.v1.custom_fields.with_streaming_response.delete(
            custom_field_ids=[0],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            custom_field = response.parse()
            assert_matches_type(CustomFieldDeleteResponse, custom_field, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncCustomFields:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncConnecteamAPISDK) -> None:
        custom_field = await async_client.users.v1.custom_fields.create(
            custom_fields=[
                {
                    "category_id": 0,
                    "is_editable_for_all_admins": True,
                    "is_editable_for_users": True,
                    "is_multi_select": True,
                    "is_required": True,
                    "is_visible_to_all_admins": True,
                    "is_visible_to_users": True,
                    "name": "name",
                }
            ],
        )
        assert_matches_type(APIResponseGetCustomFieldsSettings, custom_field, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.users.v1.custom_fields.with_raw_response.create(
            custom_fields=[
                {
                    "category_id": 0,
                    "is_editable_for_all_admins": True,
                    "is_editable_for_users": True,
                    "is_multi_select": True,
                    "is_required": True,
                    "is_visible_to_all_admins": True,
                    "is_visible_to_users": True,
                    "name": "name",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        custom_field = await response.parse()
        assert_matches_type(APIResponseGetCustomFieldsSettings, custom_field, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.users.v1.custom_fields.with_streaming_response.create(
            custom_fields=[
                {
                    "category_id": 0,
                    "is_editable_for_all_admins": True,
                    "is_editable_for_users": True,
                    "is_multi_select": True,
                    "is_required": True,
                    "is_visible_to_all_admins": True,
                    "is_visible_to_users": True,
                    "name": "name",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            custom_field = await response.parse()
            assert_matches_type(APIResponseGetCustomFieldsSettings, custom_field, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        custom_field = await async_client.users.v1.custom_fields.update(
            custom_fields=[{"id": 0}],
        )
        assert_matches_type(APIResponseGetCustomFieldsSettings, custom_field, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.users.v1.custom_fields.with_raw_response.update(
            custom_fields=[{"id": 0}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        custom_field = await response.parse()
        assert_matches_type(APIResponseGetCustomFieldsSettings, custom_field, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.users.v1.custom_fields.with_streaming_response.update(
            custom_fields=[{"id": 0}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            custom_field = await response.parse()
            assert_matches_type(APIResponseGetCustomFieldsSettings, custom_field, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        custom_field = await async_client.users.v1.custom_fields.list()
        assert_matches_type(CustomFieldListResponse, custom_field, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        custom_field = await async_client.users.v1.custom_fields.list(
            category_ids=[0],
            custom_field_ids=[0],
            custom_field_names=["string"],
            custom_field_types=["email"],
            limit=1,
            offset=0,
            order="asc",
            sort="id",
        )
        assert_matches_type(CustomFieldListResponse, custom_field, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.users.v1.custom_fields.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        custom_field = await response.parse()
        assert_matches_type(CustomFieldListResponse, custom_field, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.users.v1.custom_fields.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            custom_field = await response.parse()
            assert_matches_type(CustomFieldListResponse, custom_field, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncConnecteamAPISDK) -> None:
        custom_field = await async_client.users.v1.custom_fields.delete(
            custom_field_ids=[0],
        )
        assert_matches_type(CustomFieldDeleteResponse, custom_field, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.users.v1.custom_fields.with_raw_response.delete(
            custom_field_ids=[0],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        custom_field = await response.parse()
        assert_matches_type(CustomFieldDeleteResponse, custom_field, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.users.v1.custom_fields.with_streaming_response.delete(
            custom_field_ids=[0],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            custom_field = await response.parse()
            assert_matches_type(CustomFieldDeleteResponse, custom_field, path=["response"])

        assert cast(Any, response.is_closed) is True
