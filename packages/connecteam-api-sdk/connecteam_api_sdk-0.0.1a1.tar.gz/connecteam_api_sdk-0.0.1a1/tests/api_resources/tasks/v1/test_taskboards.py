# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from connecteam_api_sdk import ConnecteamAPISDK, AsyncConnecteamAPISDK
from connecteam_api_sdk.types.tasks.v1 import (
    TaskboardListResponse,
    TaskboardGetLabelsResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTaskboards:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: ConnecteamAPISDK) -> None:
        taskboard = client.tasks.v1.taskboards.list()
        assert_matches_type(TaskboardListResponse, taskboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: ConnecteamAPISDK) -> None:
        response = client.tasks.v1.taskboards.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        taskboard = response.parse()
        assert_matches_type(TaskboardListResponse, taskboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: ConnecteamAPISDK) -> None:
        with client.tasks.v1.taskboards.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            taskboard = response.parse()
            assert_matches_type(TaskboardListResponse, taskboard, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_get_labels(self, client: ConnecteamAPISDK) -> None:
        taskboard = client.tasks.v1.taskboards.get_labels(
            task_board_id="taskBoardId",
        )
        assert_matches_type(TaskboardGetLabelsResponse, taskboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_get_labels_with_all_params(self, client: ConnecteamAPISDK) -> None:
        taskboard = client.tasks.v1.taskboards.get_labels(
            task_board_id="taskBoardId",
            limit=1,
            offset=0,
            title="title",
        )
        assert_matches_type(TaskboardGetLabelsResponse, taskboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_labels(self, client: ConnecteamAPISDK) -> None:
        response = client.tasks.v1.taskboards.with_raw_response.get_labels(
            task_board_id="taskBoardId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        taskboard = response.parse()
        assert_matches_type(TaskboardGetLabelsResponse, taskboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_labels(self, client: ConnecteamAPISDK) -> None:
        with client.tasks.v1.taskboards.with_streaming_response.get_labels(
            task_board_id="taskBoardId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            taskboard = response.parse()
            assert_matches_type(TaskboardGetLabelsResponse, taskboard, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_get_labels(self, client: ConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_board_id` but received ''"):
            client.tasks.v1.taskboards.with_raw_response.get_labels(
                task_board_id="",
            )


class TestAsyncTaskboards:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        taskboard = await async_client.tasks.v1.taskboards.list()
        assert_matches_type(TaskboardListResponse, taskboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.tasks.v1.taskboards.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        taskboard = await response.parse()
        assert_matches_type(TaskboardListResponse, taskboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.tasks.v1.taskboards.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            taskboard = await response.parse()
            assert_matches_type(TaskboardListResponse, taskboard, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_labels(self, async_client: AsyncConnecteamAPISDK) -> None:
        taskboard = await async_client.tasks.v1.taskboards.get_labels(
            task_board_id="taskBoardId",
        )
        assert_matches_type(TaskboardGetLabelsResponse, taskboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_labels_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        taskboard = await async_client.tasks.v1.taskboards.get_labels(
            task_board_id="taskBoardId",
            limit=1,
            offset=0,
            title="title",
        )
        assert_matches_type(TaskboardGetLabelsResponse, taskboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_labels(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.tasks.v1.taskboards.with_raw_response.get_labels(
            task_board_id="taskBoardId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        taskboard = await response.parse()
        assert_matches_type(TaskboardGetLabelsResponse, taskboard, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_labels(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.tasks.v1.taskboards.with_streaming_response.get_labels(
            task_board_id="taskBoardId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            taskboard = await response.parse()
            assert_matches_type(TaskboardGetLabelsResponse, taskboard, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_get_labels(self, async_client: AsyncConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_board_id` but received ''"):
            await async_client.tasks.v1.taskboards.with_raw_response.get_labels(
                task_board_id="",
            )
