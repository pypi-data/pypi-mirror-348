# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from connecteam_api_sdk import ConnecteamAPISDK, AsyncConnecteamAPISDK
from connecteam_api_sdk.types.tasks.v1.taskboards import (
    TaskListResponse,
    TaskCreateResponse,
    TaskDeleteResponse,
    TaskUpdateResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTasks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: ConnecteamAPISDK) -> None:
        task = client.tasks.v1.taskboards.tasks.create(
            task_board_id="taskBoardId",
            due_date=0,
            start_time=0,
            status="draft",
            title="title",
            user_ids=[1],
        )
        assert_matches_type(TaskCreateResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: ConnecteamAPISDK) -> None:
        task = client.tasks.v1.taskboards.tasks.create(
            task_board_id="taskBoardId",
            due_date=0,
            start_time=0,
            status="draft",
            title="title",
            user_ids=[1],
            description={"content": "content"},
            is_archived=True,
            label_ids=["string"],
            type="oneTime",
        )
        assert_matches_type(TaskCreateResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: ConnecteamAPISDK) -> None:
        response = client.tasks.v1.taskboards.tasks.with_raw_response.create(
            task_board_id="taskBoardId",
            due_date=0,
            start_time=0,
            status="draft",
            title="title",
            user_ids=[1],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = response.parse()
        assert_matches_type(TaskCreateResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: ConnecteamAPISDK) -> None:
        with client.tasks.v1.taskboards.tasks.with_streaming_response.create(
            task_board_id="taskBoardId",
            due_date=0,
            start_time=0,
            status="draft",
            title="title",
            user_ids=[1],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = response.parse()
            assert_matches_type(TaskCreateResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_create(self, client: ConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_board_id` but received ''"):
            client.tasks.v1.taskboards.tasks.with_raw_response.create(
                task_board_id="",
                due_date=0,
                start_time=0,
                status="draft",
                title="title",
                user_ids=[1],
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: ConnecteamAPISDK) -> None:
        task = client.tasks.v1.taskboards.tasks.update(
            task_id="taskId",
            task_board_id="taskBoardId",
            due_date=0,
            start_time=0,
            status="draft",
            title="title",
            user_ids=[1],
        )
        assert_matches_type(TaskUpdateResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: ConnecteamAPISDK) -> None:
        task = client.tasks.v1.taskboards.tasks.update(
            task_id="taskId",
            task_board_id="taskBoardId",
            due_date=0,
            start_time=0,
            status="draft",
            title="title",
            user_ids=[1],
            is_archived=True,
            label_ids=["string"],
            type="oneTime",
        )
        assert_matches_type(TaskUpdateResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: ConnecteamAPISDK) -> None:
        response = client.tasks.v1.taskboards.tasks.with_raw_response.update(
            task_id="taskId",
            task_board_id="taskBoardId",
            due_date=0,
            start_time=0,
            status="draft",
            title="title",
            user_ids=[1],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = response.parse()
        assert_matches_type(TaskUpdateResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: ConnecteamAPISDK) -> None:
        with client.tasks.v1.taskboards.tasks.with_streaming_response.update(
            task_id="taskId",
            task_board_id="taskBoardId",
            due_date=0,
            start_time=0,
            status="draft",
            title="title",
            user_ids=[1],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = response.parse()
            assert_matches_type(TaskUpdateResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: ConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_board_id` but received ''"):
            client.tasks.v1.taskboards.tasks.with_raw_response.update(
                task_id="taskId",
                task_board_id="",
                due_date=0,
                start_time=0,
                status="draft",
                title="title",
                user_ids=[1],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            client.tasks.v1.taskboards.tasks.with_raw_response.update(
                task_id="",
                task_board_id="taskBoardId",
                due_date=0,
                start_time=0,
                status="draft",
                title="title",
                user_ids=[1],
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: ConnecteamAPISDK) -> None:
        task = client.tasks.v1.taskboards.tasks.list(
            task_board_id="taskBoardId",
        )
        assert_matches_type(TaskListResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: ConnecteamAPISDK) -> None:
        task = client.tasks.v1.taskboards.tasks.list(
            task_board_id="taskBoardId",
            label_ids=["string"],
            limit=1,
            offset=0,
            status="draft",
            task_ids=["string"],
            user_ids=[0],
        )
        assert_matches_type(TaskListResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: ConnecteamAPISDK) -> None:
        response = client.tasks.v1.taskboards.tasks.with_raw_response.list(
            task_board_id="taskBoardId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = response.parse()
        assert_matches_type(TaskListResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: ConnecteamAPISDK) -> None:
        with client.tasks.v1.taskboards.tasks.with_streaming_response.list(
            task_board_id="taskBoardId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = response.parse()
            assert_matches_type(TaskListResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_list(self, client: ConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_board_id` but received ''"):
            client.tasks.v1.taskboards.tasks.with_raw_response.list(
                task_board_id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: ConnecteamAPISDK) -> None:
        task = client.tasks.v1.taskboards.tasks.delete(
            task_id="taskId",
            task_board_id="taskBoardId",
        )
        assert_matches_type(TaskDeleteResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: ConnecteamAPISDK) -> None:
        response = client.tasks.v1.taskboards.tasks.with_raw_response.delete(
            task_id="taskId",
            task_board_id="taskBoardId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = response.parse()
        assert_matches_type(TaskDeleteResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: ConnecteamAPISDK) -> None:
        with client.tasks.v1.taskboards.tasks.with_streaming_response.delete(
            task_id="taskId",
            task_board_id="taskBoardId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = response.parse()
            assert_matches_type(TaskDeleteResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: ConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_board_id` but received ''"):
            client.tasks.v1.taskboards.tasks.with_raw_response.delete(
                task_id="taskId",
                task_board_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            client.tasks.v1.taskboards.tasks.with_raw_response.delete(
                task_id="",
                task_board_id="taskBoardId",
            )


class TestAsyncTasks:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncConnecteamAPISDK) -> None:
        task = await async_client.tasks.v1.taskboards.tasks.create(
            task_board_id="taskBoardId",
            due_date=0,
            start_time=0,
            status="draft",
            title="title",
            user_ids=[1],
        )
        assert_matches_type(TaskCreateResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        task = await async_client.tasks.v1.taskboards.tasks.create(
            task_board_id="taskBoardId",
            due_date=0,
            start_time=0,
            status="draft",
            title="title",
            user_ids=[1],
            description={"content": "content"},
            is_archived=True,
            label_ids=["string"],
            type="oneTime",
        )
        assert_matches_type(TaskCreateResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.tasks.v1.taskboards.tasks.with_raw_response.create(
            task_board_id="taskBoardId",
            due_date=0,
            start_time=0,
            status="draft",
            title="title",
            user_ids=[1],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = await response.parse()
        assert_matches_type(TaskCreateResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.tasks.v1.taskboards.tasks.with_streaming_response.create(
            task_board_id="taskBoardId",
            due_date=0,
            start_time=0,
            status="draft",
            title="title",
            user_ids=[1],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = await response.parse()
            assert_matches_type(TaskCreateResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_create(self, async_client: AsyncConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_board_id` but received ''"):
            await async_client.tasks.v1.taskboards.tasks.with_raw_response.create(
                task_board_id="",
                due_date=0,
                start_time=0,
                status="draft",
                title="title",
                user_ids=[1],
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        task = await async_client.tasks.v1.taskboards.tasks.update(
            task_id="taskId",
            task_board_id="taskBoardId",
            due_date=0,
            start_time=0,
            status="draft",
            title="title",
            user_ids=[1],
        )
        assert_matches_type(TaskUpdateResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        task = await async_client.tasks.v1.taskboards.tasks.update(
            task_id="taskId",
            task_board_id="taskBoardId",
            due_date=0,
            start_time=0,
            status="draft",
            title="title",
            user_ids=[1],
            is_archived=True,
            label_ids=["string"],
            type="oneTime",
        )
        assert_matches_type(TaskUpdateResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.tasks.v1.taskboards.tasks.with_raw_response.update(
            task_id="taskId",
            task_board_id="taskBoardId",
            due_date=0,
            start_time=0,
            status="draft",
            title="title",
            user_ids=[1],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = await response.parse()
        assert_matches_type(TaskUpdateResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.tasks.v1.taskboards.tasks.with_streaming_response.update(
            task_id="taskId",
            task_board_id="taskBoardId",
            due_date=0,
            start_time=0,
            status="draft",
            title="title",
            user_ids=[1],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = await response.parse()
            assert_matches_type(TaskUpdateResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_board_id` but received ''"):
            await async_client.tasks.v1.taskboards.tasks.with_raw_response.update(
                task_id="taskId",
                task_board_id="",
                due_date=0,
                start_time=0,
                status="draft",
                title="title",
                user_ids=[1],
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            await async_client.tasks.v1.taskboards.tasks.with_raw_response.update(
                task_id="",
                task_board_id="taskBoardId",
                due_date=0,
                start_time=0,
                status="draft",
                title="title",
                user_ids=[1],
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        task = await async_client.tasks.v1.taskboards.tasks.list(
            task_board_id="taskBoardId",
        )
        assert_matches_type(TaskListResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        task = await async_client.tasks.v1.taskboards.tasks.list(
            task_board_id="taskBoardId",
            label_ids=["string"],
            limit=1,
            offset=0,
            status="draft",
            task_ids=["string"],
            user_ids=[0],
        )
        assert_matches_type(TaskListResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.tasks.v1.taskboards.tasks.with_raw_response.list(
            task_board_id="taskBoardId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = await response.parse()
        assert_matches_type(TaskListResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.tasks.v1.taskboards.tasks.with_streaming_response.list(
            task_board_id="taskBoardId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = await response.parse()
            assert_matches_type(TaskListResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_board_id` but received ''"):
            await async_client.tasks.v1.taskboards.tasks.with_raw_response.list(
                task_board_id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncConnecteamAPISDK) -> None:
        task = await async_client.tasks.v1.taskboards.tasks.delete(
            task_id="taskId",
            task_board_id="taskBoardId",
        )
        assert_matches_type(TaskDeleteResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.tasks.v1.taskboards.tasks.with_raw_response.delete(
            task_id="taskId",
            task_board_id="taskBoardId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = await response.parse()
        assert_matches_type(TaskDeleteResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.tasks.v1.taskboards.tasks.with_streaming_response.delete(
            task_id="taskId",
            task_board_id="taskBoardId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = await response.parse()
            assert_matches_type(TaskDeleteResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_board_id` but received ''"):
            await async_client.tasks.v1.taskboards.tasks.with_raw_response.delete(
                task_id="taskId",
                task_board_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            await async_client.tasks.v1.taskboards.tasks.with_raw_response.delete(
                task_id="",
                task_board_id="taskBoardId",
            )
