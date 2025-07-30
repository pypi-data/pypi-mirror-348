# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from connecteam_api_sdk import ConnecteamAPISDK, AsyncConnecteamAPISDK
from connecteam_api_sdk.types.scheduler.v1.schedulers import (
    ShiftLayerListResponse,
    ShiftLayerGetValuesResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestShiftLayers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: ConnecteamAPISDK) -> None:
        shift_layer = client.scheduler.v1.schedulers.shift_layers.list(
            0,
        )
        assert_matches_type(ShiftLayerListResponse, shift_layer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: ConnecteamAPISDK) -> None:
        response = client.scheduler.v1.schedulers.shift_layers.with_raw_response.list(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        shift_layer = response.parse()
        assert_matches_type(ShiftLayerListResponse, shift_layer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: ConnecteamAPISDK) -> None:
        with client.scheduler.v1.schedulers.shift_layers.with_streaming_response.list(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            shift_layer = response.parse()
            assert_matches_type(ShiftLayerListResponse, shift_layer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_get_values(self, client: ConnecteamAPISDK) -> None:
        shift_layer = client.scheduler.v1.schedulers.shift_layers.get_values(
            layer_id="layerId",
            scheduler_id=0,
        )
        assert_matches_type(ShiftLayerGetValuesResponse, shift_layer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_get_values_with_all_params(self, client: ConnecteamAPISDK) -> None:
        shift_layer = client.scheduler.v1.schedulers.shift_layers.get_values(
            layer_id="layerId",
            scheduler_id=0,
            limit=1,
            offset=0,
        )
        assert_matches_type(ShiftLayerGetValuesResponse, shift_layer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_values(self, client: ConnecteamAPISDK) -> None:
        response = client.scheduler.v1.schedulers.shift_layers.with_raw_response.get_values(
            layer_id="layerId",
            scheduler_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        shift_layer = response.parse()
        assert_matches_type(ShiftLayerGetValuesResponse, shift_layer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_values(self, client: ConnecteamAPISDK) -> None:
        with client.scheduler.v1.schedulers.shift_layers.with_streaming_response.get_values(
            layer_id="layerId",
            scheduler_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            shift_layer = response.parse()
            assert_matches_type(ShiftLayerGetValuesResponse, shift_layer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_get_values(self, client: ConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `layer_id` but received ''"):
            client.scheduler.v1.schedulers.shift_layers.with_raw_response.get_values(
                layer_id="",
                scheduler_id=0,
            )


class TestAsyncShiftLayers:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        shift_layer = await async_client.scheduler.v1.schedulers.shift_layers.list(
            0,
        )
        assert_matches_type(ShiftLayerListResponse, shift_layer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.scheduler.v1.schedulers.shift_layers.with_raw_response.list(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        shift_layer = await response.parse()
        assert_matches_type(ShiftLayerListResponse, shift_layer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.scheduler.v1.schedulers.shift_layers.with_streaming_response.list(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            shift_layer = await response.parse()
            assert_matches_type(ShiftLayerListResponse, shift_layer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_values(self, async_client: AsyncConnecteamAPISDK) -> None:
        shift_layer = await async_client.scheduler.v1.schedulers.shift_layers.get_values(
            layer_id="layerId",
            scheduler_id=0,
        )
        assert_matches_type(ShiftLayerGetValuesResponse, shift_layer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_values_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        shift_layer = await async_client.scheduler.v1.schedulers.shift_layers.get_values(
            layer_id="layerId",
            scheduler_id=0,
            limit=1,
            offset=0,
        )
        assert_matches_type(ShiftLayerGetValuesResponse, shift_layer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_values(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.scheduler.v1.schedulers.shift_layers.with_raw_response.get_values(
            layer_id="layerId",
            scheduler_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        shift_layer = await response.parse()
        assert_matches_type(ShiftLayerGetValuesResponse, shift_layer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_values(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.scheduler.v1.schedulers.shift_layers.with_streaming_response.get_values(
            layer_id="layerId",
            scheduler_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            shift_layer = await response.parse()
            assert_matches_type(ShiftLayerGetValuesResponse, shift_layer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_get_values(self, async_client: AsyncConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `layer_id` but received ''"):
            await async_client.scheduler.v1.schedulers.shift_layers.with_raw_response.get_values(
                layer_id="",
                scheduler_id=0,
            )
