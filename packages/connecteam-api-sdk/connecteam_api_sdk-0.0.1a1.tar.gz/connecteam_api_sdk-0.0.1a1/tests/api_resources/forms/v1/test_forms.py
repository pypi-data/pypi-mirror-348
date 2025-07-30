# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from connecteam_api_sdk import ConnecteamAPISDK, AsyncConnecteamAPISDK
from connecteam_api_sdk.types.forms.v1 import FormListResponse, FormRetrieveResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestForms:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: ConnecteamAPISDK) -> None:
        form = client.forms.v1.forms.retrieve(
            1,
        )
        assert_matches_type(FormRetrieveResponse, form, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: ConnecteamAPISDK) -> None:
        response = client.forms.v1.forms.with_raw_response.retrieve(
            1,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        form = response.parse()
        assert_matches_type(FormRetrieveResponse, form, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: ConnecteamAPISDK) -> None:
        with client.forms.v1.forms.with_streaming_response.retrieve(
            1,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            form = response.parse()
            assert_matches_type(FormRetrieveResponse, form, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: ConnecteamAPISDK) -> None:
        form = client.forms.v1.forms.list()
        assert_matches_type(FormListResponse, form, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: ConnecteamAPISDK) -> None:
        form = client.forms.v1.forms.list(
            limit=1,
            offset=0,
        )
        assert_matches_type(FormListResponse, form, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: ConnecteamAPISDK) -> None:
        response = client.forms.v1.forms.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        form = response.parse()
        assert_matches_type(FormListResponse, form, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: ConnecteamAPISDK) -> None:
        with client.forms.v1.forms.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            form = response.parse()
            assert_matches_type(FormListResponse, form, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncForms:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncConnecteamAPISDK) -> None:
        form = await async_client.forms.v1.forms.retrieve(
            1,
        )
        assert_matches_type(FormRetrieveResponse, form, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.forms.v1.forms.with_raw_response.retrieve(
            1,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        form = await response.parse()
        assert_matches_type(FormRetrieveResponse, form, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.forms.v1.forms.with_streaming_response.retrieve(
            1,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            form = await response.parse()
            assert_matches_type(FormRetrieveResponse, form, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        form = await async_client.forms.v1.forms.list()
        assert_matches_type(FormListResponse, form, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        form = await async_client.forms.v1.forms.list(
            limit=1,
            offset=0,
        )
        assert_matches_type(FormListResponse, form, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.forms.v1.forms.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        form = await response.parse()
        assert_matches_type(FormListResponse, form, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.forms.v1.forms.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            form = await response.parse()
            assert_matches_type(FormListResponse, form, path=["response"])

        assert cast(Any, response.is_closed) is True
