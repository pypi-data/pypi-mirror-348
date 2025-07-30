# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from connecteam_api_sdk import ConnecteamAPISDK, AsyncConnecteamAPISDK
from connecteam_api_sdk.types.daily_info.v1 import DailyNoteResponse, DailyNoteDeleteResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDailyNote:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: ConnecteamAPISDK) -> None:
        daily_note = client.daily_info.v1.daily_note.retrieve(
            0,
        )
        assert_matches_type(DailyNoteResponse, daily_note, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: ConnecteamAPISDK) -> None:
        response = client.daily_info.v1.daily_note.with_raw_response.retrieve(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        daily_note = response.parse()
        assert_matches_type(DailyNoteResponse, daily_note, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: ConnecteamAPISDK) -> None:
        with client.daily_info.v1.daily_note.with_streaming_response.retrieve(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            daily_note = response.parse()
            assert_matches_type(DailyNoteResponse, daily_note, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: ConnecteamAPISDK) -> None:
        daily_note = client.daily_info.v1.daily_note.update(
            note_id=0,
        )
        assert_matches_type(DailyNoteResponse, daily_note, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: ConnecteamAPISDK) -> None:
        daily_note = client.daily_info.v1.daily_note.update(
            note_id=0,
            qualified_group_ids=[0],
            qualified_user_ids=[1],
            title="title",
        )
        assert_matches_type(DailyNoteResponse, daily_note, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: ConnecteamAPISDK) -> None:
        response = client.daily_info.v1.daily_note.with_raw_response.update(
            note_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        daily_note = response.parse()
        assert_matches_type(DailyNoteResponse, daily_note, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: ConnecteamAPISDK) -> None:
        with client.daily_info.v1.daily_note.with_streaming_response.update(
            note_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            daily_note = response.parse()
            assert_matches_type(DailyNoteResponse, daily_note, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: ConnecteamAPISDK) -> None:
        daily_note = client.daily_info.v1.daily_note.delete(
            0,
        )
        assert_matches_type(DailyNoteDeleteResponse, daily_note, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: ConnecteamAPISDK) -> None:
        response = client.daily_info.v1.daily_note.with_raw_response.delete(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        daily_note = response.parse()
        assert_matches_type(DailyNoteDeleteResponse, daily_note, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: ConnecteamAPISDK) -> None:
        with client.daily_info.v1.daily_note.with_streaming_response.delete(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            daily_note = response.parse()
            assert_matches_type(DailyNoteDeleteResponse, daily_note, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDailyNote:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncConnecteamAPISDK) -> None:
        daily_note = await async_client.daily_info.v1.daily_note.retrieve(
            0,
        )
        assert_matches_type(DailyNoteResponse, daily_note, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.daily_info.v1.daily_note.with_raw_response.retrieve(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        daily_note = await response.parse()
        assert_matches_type(DailyNoteResponse, daily_note, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.daily_info.v1.daily_note.with_streaming_response.retrieve(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            daily_note = await response.parse()
            assert_matches_type(DailyNoteResponse, daily_note, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        daily_note = await async_client.daily_info.v1.daily_note.update(
            note_id=0,
        )
        assert_matches_type(DailyNoteResponse, daily_note, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        daily_note = await async_client.daily_info.v1.daily_note.update(
            note_id=0,
            qualified_group_ids=[0],
            qualified_user_ids=[1],
            title="title",
        )
        assert_matches_type(DailyNoteResponse, daily_note, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.daily_info.v1.daily_note.with_raw_response.update(
            note_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        daily_note = await response.parse()
        assert_matches_type(DailyNoteResponse, daily_note, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.daily_info.v1.daily_note.with_streaming_response.update(
            note_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            daily_note = await response.parse()
            assert_matches_type(DailyNoteResponse, daily_note, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncConnecteamAPISDK) -> None:
        daily_note = await async_client.daily_info.v1.daily_note.delete(
            0,
        )
        assert_matches_type(DailyNoteDeleteResponse, daily_note, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.daily_info.v1.daily_note.with_raw_response.delete(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        daily_note = await response.parse()
        assert_matches_type(DailyNoteDeleteResponse, daily_note, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.daily_info.v1.daily_note.with_streaming_response.delete(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            daily_note = await response.parse()
            assert_matches_type(DailyNoteDeleteResponse, daily_note, path=["response"])

        assert cast(Any, response.is_closed) is True
