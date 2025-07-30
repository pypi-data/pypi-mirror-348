# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from connecteam_api_sdk import ConnecteamAPISDK, AsyncConnecteamAPISDK
from connecteam_api_sdk.types.users.v1.custom_fields import (
    APIResponseBase,
    OptionListResponse,
    APIResponseDropdownCustomFieldOption,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestOptions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: ConnecteamAPISDK) -> None:
        option = client.users.v1.custom_fields.options.create(
            custom_field_id=0,
            value="value",
        )
        assert_matches_type(APIResponseDropdownCustomFieldOption, option, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: ConnecteamAPISDK) -> None:
        option = client.users.v1.custom_fields.options.create(
            custom_field_id=0,
            value="value",
            is_disabled=True,
        )
        assert_matches_type(APIResponseDropdownCustomFieldOption, option, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: ConnecteamAPISDK) -> None:
        response = client.users.v1.custom_fields.options.with_raw_response.create(
            custom_field_id=0,
            value="value",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        option = response.parse()
        assert_matches_type(APIResponseDropdownCustomFieldOption, option, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: ConnecteamAPISDK) -> None:
        with client.users.v1.custom_fields.options.with_streaming_response.create(
            custom_field_id=0,
            value="value",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            option = response.parse()
            assert_matches_type(APIResponseDropdownCustomFieldOption, option, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: ConnecteamAPISDK) -> None:
        option = client.users.v1.custom_fields.options.update(
            option_id=0,
            custom_field_id=0,
        )
        assert_matches_type(APIResponseDropdownCustomFieldOption, option, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: ConnecteamAPISDK) -> None:
        option = client.users.v1.custom_fields.options.update(
            option_id=0,
            custom_field_id=0,
            is_disabled=True,
            value="value",
        )
        assert_matches_type(APIResponseDropdownCustomFieldOption, option, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: ConnecteamAPISDK) -> None:
        response = client.users.v1.custom_fields.options.with_raw_response.update(
            option_id=0,
            custom_field_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        option = response.parse()
        assert_matches_type(APIResponseDropdownCustomFieldOption, option, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: ConnecteamAPISDK) -> None:
        with client.users.v1.custom_fields.options.with_streaming_response.update(
            option_id=0,
            custom_field_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            option = response.parse()
            assert_matches_type(APIResponseDropdownCustomFieldOption, option, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: ConnecteamAPISDK) -> None:
        option = client.users.v1.custom_fields.options.list(
            custom_field_id=0,
        )
        assert_matches_type(OptionListResponse, option, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: ConnecteamAPISDK) -> None:
        option = client.users.v1.custom_fields.options.list(
            custom_field_id=0,
            is_deleted=True,
            is_disabled=True,
            limit=1,
            offset=0,
        )
        assert_matches_type(OptionListResponse, option, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: ConnecteamAPISDK) -> None:
        response = client.users.v1.custom_fields.options.with_raw_response.list(
            custom_field_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        option = response.parse()
        assert_matches_type(OptionListResponse, option, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: ConnecteamAPISDK) -> None:
        with client.users.v1.custom_fields.options.with_streaming_response.list(
            custom_field_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            option = response.parse()
            assert_matches_type(OptionListResponse, option, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: ConnecteamAPISDK) -> None:
        option = client.users.v1.custom_fields.options.delete(
            option_id=0,
            custom_field_id=0,
        )
        assert_matches_type(APIResponseBase, option, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: ConnecteamAPISDK) -> None:
        response = client.users.v1.custom_fields.options.with_raw_response.delete(
            option_id=0,
            custom_field_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        option = response.parse()
        assert_matches_type(APIResponseBase, option, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: ConnecteamAPISDK) -> None:
        with client.users.v1.custom_fields.options.with_streaming_response.delete(
            option_id=0,
            custom_field_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            option = response.parse()
            assert_matches_type(APIResponseBase, option, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncOptions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncConnecteamAPISDK) -> None:
        option = await async_client.users.v1.custom_fields.options.create(
            custom_field_id=0,
            value="value",
        )
        assert_matches_type(APIResponseDropdownCustomFieldOption, option, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        option = await async_client.users.v1.custom_fields.options.create(
            custom_field_id=0,
            value="value",
            is_disabled=True,
        )
        assert_matches_type(APIResponseDropdownCustomFieldOption, option, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.users.v1.custom_fields.options.with_raw_response.create(
            custom_field_id=0,
            value="value",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        option = await response.parse()
        assert_matches_type(APIResponseDropdownCustomFieldOption, option, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.users.v1.custom_fields.options.with_streaming_response.create(
            custom_field_id=0,
            value="value",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            option = await response.parse()
            assert_matches_type(APIResponseDropdownCustomFieldOption, option, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        option = await async_client.users.v1.custom_fields.options.update(
            option_id=0,
            custom_field_id=0,
        )
        assert_matches_type(APIResponseDropdownCustomFieldOption, option, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        option = await async_client.users.v1.custom_fields.options.update(
            option_id=0,
            custom_field_id=0,
            is_disabled=True,
            value="value",
        )
        assert_matches_type(APIResponseDropdownCustomFieldOption, option, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.users.v1.custom_fields.options.with_raw_response.update(
            option_id=0,
            custom_field_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        option = await response.parse()
        assert_matches_type(APIResponseDropdownCustomFieldOption, option, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.users.v1.custom_fields.options.with_streaming_response.update(
            option_id=0,
            custom_field_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            option = await response.parse()
            assert_matches_type(APIResponseDropdownCustomFieldOption, option, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        option = await async_client.users.v1.custom_fields.options.list(
            custom_field_id=0,
        )
        assert_matches_type(OptionListResponse, option, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        option = await async_client.users.v1.custom_fields.options.list(
            custom_field_id=0,
            is_deleted=True,
            is_disabled=True,
            limit=1,
            offset=0,
        )
        assert_matches_type(OptionListResponse, option, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.users.v1.custom_fields.options.with_raw_response.list(
            custom_field_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        option = await response.parse()
        assert_matches_type(OptionListResponse, option, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.users.v1.custom_fields.options.with_streaming_response.list(
            custom_field_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            option = await response.parse()
            assert_matches_type(OptionListResponse, option, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncConnecteamAPISDK) -> None:
        option = await async_client.users.v1.custom_fields.options.delete(
            option_id=0,
            custom_field_id=0,
        )
        assert_matches_type(APIResponseBase, option, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.users.v1.custom_fields.options.with_raw_response.delete(
            option_id=0,
            custom_field_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        option = await response.parse()
        assert_matches_type(APIResponseBase, option, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.users.v1.custom_fields.options.with_streaming_response.delete(
            option_id=0,
            custom_field_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            option = await response.parse()
            assert_matches_type(APIResponseBase, option, path=["response"])

        assert cast(Any, response.is_closed) is True
