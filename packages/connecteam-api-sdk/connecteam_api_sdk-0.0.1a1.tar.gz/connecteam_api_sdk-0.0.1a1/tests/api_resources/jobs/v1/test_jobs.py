# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from connecteam_api_sdk import ConnecteamAPISDK, AsyncConnecteamAPISDK
from connecteam_api_sdk.types.jobs.v1 import (
    APIResponse,
    JobListResponse,
    JobCreateResponse,
    JobDeleteResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestJobs:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: ConnecteamAPISDK) -> None:
        job = client.jobs.v1.jobs.create(
            body=[
                {
                    "instance_ids": [0],
                    "title": "title",
                }
            ],
        )
        assert_matches_type(JobCreateResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: ConnecteamAPISDK) -> None:
        response = client.jobs.v1.jobs.with_raw_response.create(
            body=[
                {
                    "instance_ids": [0],
                    "title": "title",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = response.parse()
        assert_matches_type(JobCreateResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: ConnecteamAPISDK) -> None:
        with client.jobs.v1.jobs.with_streaming_response.create(
            body=[
                {
                    "instance_ids": [0],
                    "title": "title",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = response.parse()
            assert_matches_type(JobCreateResponse, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: ConnecteamAPISDK) -> None:
        job = client.jobs.v1.jobs.retrieve(
            "jobId",
        )
        assert_matches_type(APIResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: ConnecteamAPISDK) -> None:
        response = client.jobs.v1.jobs.with_raw_response.retrieve(
            "jobId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = response.parse()
        assert_matches_type(APIResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: ConnecteamAPISDK) -> None:
        with client.jobs.v1.jobs.with_streaming_response.retrieve(
            "jobId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = response.parse()
            assert_matches_type(APIResponse, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: ConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_id` but received ''"):
            client.jobs.v1.jobs.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update_overload_1(self, client: ConnecteamAPISDK) -> None:
        job = client.jobs.v1.jobs.update(
            job_id="jobId",
            parent_id="parentId",
            title="title",
            use_parent_data=True,
        )
        assert_matches_type(APIResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params_overload_1(self, client: ConnecteamAPISDK) -> None:
        job = client.jobs.v1.jobs.update(
            job_id="jobId",
            parent_id="parentId",
            title="title",
            use_parent_data=True,
            assign={
                "group_ids": [1],
                "type": "users",
                "user_ids": [1],
            },
            code="code",
            description="description",
            gps={
                "address": "address",
                "latitude": 0,
                "longitude": 0,
            },
        )
        assert_matches_type(APIResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update_overload_1(self, client: ConnecteamAPISDK) -> None:
        response = client.jobs.v1.jobs.with_raw_response.update(
            job_id="jobId",
            parent_id="parentId",
            title="title",
            use_parent_data=True,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = response.parse()
        assert_matches_type(APIResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update_overload_1(self, client: ConnecteamAPISDK) -> None:
        with client.jobs.v1.jobs.with_streaming_response.update(
            job_id="jobId",
            parent_id="parentId",
            title="title",
            use_parent_data=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = response.parse()
            assert_matches_type(APIResponse, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update_overload_1(self, client: ConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_id` but received ''"):
            client.jobs.v1.jobs.with_raw_response.update(
                job_id="",
                parent_id="parentId",
                title="title",
                use_parent_data=True,
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update_overload_2(self, client: ConnecteamAPISDK) -> None:
        job = client.jobs.v1.jobs.update(
            job_id="jobId",
            title="title",
        )
        assert_matches_type(APIResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params_overload_2(self, client: ConnecteamAPISDK) -> None:
        job = client.jobs.v1.jobs.update(
            job_id="jobId",
            title="title",
            assign={
                "group_ids": [1],
                "type": "users",
                "user_ids": [1],
            },
            code="code",
            color="color",
            description="description",
            gps={
                "address": "address",
                "latitude": 0,
                "longitude": 0,
            },
            instance_ids=[0],
        )
        assert_matches_type(APIResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update_overload_2(self, client: ConnecteamAPISDK) -> None:
        response = client.jobs.v1.jobs.with_raw_response.update(
            job_id="jobId",
            title="title",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = response.parse()
        assert_matches_type(APIResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update_overload_2(self, client: ConnecteamAPISDK) -> None:
        with client.jobs.v1.jobs.with_streaming_response.update(
            job_id="jobId",
            title="title",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = response.parse()
            assert_matches_type(APIResponse, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update_overload_2(self, client: ConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_id` but received ''"):
            client.jobs.v1.jobs.with_raw_response.update(
                job_id="",
                title="title",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: ConnecteamAPISDK) -> None:
        job = client.jobs.v1.jobs.list()
        assert_matches_type(JobListResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: ConnecteamAPISDK) -> None:
        job = client.jobs.v1.jobs.list(
            include_deleted=True,
            instance_ids=[0],
            job_codes=["string"],
            job_ids=["string"],
            job_names=["string"],
            limit=1,
            offset=0,
            order="asc",
            sort="title",
        )
        assert_matches_type(JobListResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: ConnecteamAPISDK) -> None:
        response = client.jobs.v1.jobs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = response.parse()
        assert_matches_type(JobListResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: ConnecteamAPISDK) -> None:
        with client.jobs.v1.jobs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = response.parse()
            assert_matches_type(JobListResponse, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: ConnecteamAPISDK) -> None:
        job = client.jobs.v1.jobs.delete(
            "jobId",
        )
        assert_matches_type(JobDeleteResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: ConnecteamAPISDK) -> None:
        response = client.jobs.v1.jobs.with_raw_response.delete(
            "jobId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = response.parse()
        assert_matches_type(JobDeleteResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: ConnecteamAPISDK) -> None:
        with client.jobs.v1.jobs.with_streaming_response.delete(
            "jobId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = response.parse()
            assert_matches_type(JobDeleteResponse, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: ConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_id` but received ''"):
            client.jobs.v1.jobs.with_raw_response.delete(
                "",
            )


class TestAsyncJobs:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncConnecteamAPISDK) -> None:
        job = await async_client.jobs.v1.jobs.create(
            body=[
                {
                    "instance_ids": [0],
                    "title": "title",
                }
            ],
        )
        assert_matches_type(JobCreateResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.jobs.v1.jobs.with_raw_response.create(
            body=[
                {
                    "instance_ids": [0],
                    "title": "title",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = await response.parse()
        assert_matches_type(JobCreateResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.jobs.v1.jobs.with_streaming_response.create(
            body=[
                {
                    "instance_ids": [0],
                    "title": "title",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = await response.parse()
            assert_matches_type(JobCreateResponse, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncConnecteamAPISDK) -> None:
        job = await async_client.jobs.v1.jobs.retrieve(
            "jobId",
        )
        assert_matches_type(APIResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.jobs.v1.jobs.with_raw_response.retrieve(
            "jobId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = await response.parse()
        assert_matches_type(APIResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.jobs.v1.jobs.with_streaming_response.retrieve(
            "jobId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = await response.parse()
            assert_matches_type(APIResponse, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_id` but received ''"):
            await async_client.jobs.v1.jobs.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_overload_1(self, async_client: AsyncConnecteamAPISDK) -> None:
        job = await async_client.jobs.v1.jobs.update(
            job_id="jobId",
            parent_id="parentId",
            title="title",
            use_parent_data=True,
        )
        assert_matches_type(APIResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params_overload_1(self, async_client: AsyncConnecteamAPISDK) -> None:
        job = await async_client.jobs.v1.jobs.update(
            job_id="jobId",
            parent_id="parentId",
            title="title",
            use_parent_data=True,
            assign={
                "group_ids": [1],
                "type": "users",
                "user_ids": [1],
            },
            code="code",
            description="description",
            gps={
                "address": "address",
                "latitude": 0,
                "longitude": 0,
            },
        )
        assert_matches_type(APIResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update_overload_1(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.jobs.v1.jobs.with_raw_response.update(
            job_id="jobId",
            parent_id="parentId",
            title="title",
            use_parent_data=True,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = await response.parse()
        assert_matches_type(APIResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update_overload_1(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.jobs.v1.jobs.with_streaming_response.update(
            job_id="jobId",
            parent_id="parentId",
            title="title",
            use_parent_data=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = await response.parse()
            assert_matches_type(APIResponse, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update_overload_1(self, async_client: AsyncConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_id` but received ''"):
            await async_client.jobs.v1.jobs.with_raw_response.update(
                job_id="",
                parent_id="parentId",
                title="title",
                use_parent_data=True,
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_overload_2(self, async_client: AsyncConnecteamAPISDK) -> None:
        job = await async_client.jobs.v1.jobs.update(
            job_id="jobId",
            title="title",
        )
        assert_matches_type(APIResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params_overload_2(self, async_client: AsyncConnecteamAPISDK) -> None:
        job = await async_client.jobs.v1.jobs.update(
            job_id="jobId",
            title="title",
            assign={
                "group_ids": [1],
                "type": "users",
                "user_ids": [1],
            },
            code="code",
            color="color",
            description="description",
            gps={
                "address": "address",
                "latitude": 0,
                "longitude": 0,
            },
            instance_ids=[0],
        )
        assert_matches_type(APIResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update_overload_2(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.jobs.v1.jobs.with_raw_response.update(
            job_id="jobId",
            title="title",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = await response.parse()
        assert_matches_type(APIResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update_overload_2(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.jobs.v1.jobs.with_streaming_response.update(
            job_id="jobId",
            title="title",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = await response.parse()
            assert_matches_type(APIResponse, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update_overload_2(self, async_client: AsyncConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_id` but received ''"):
            await async_client.jobs.v1.jobs.with_raw_response.update(
                job_id="",
                title="title",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        job = await async_client.jobs.v1.jobs.list()
        assert_matches_type(JobListResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        job = await async_client.jobs.v1.jobs.list(
            include_deleted=True,
            instance_ids=[0],
            job_codes=["string"],
            job_ids=["string"],
            job_names=["string"],
            limit=1,
            offset=0,
            order="asc",
            sort="title",
        )
        assert_matches_type(JobListResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.jobs.v1.jobs.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = await response.parse()
        assert_matches_type(JobListResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.jobs.v1.jobs.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = await response.parse()
            assert_matches_type(JobListResponse, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncConnecteamAPISDK) -> None:
        job = await async_client.jobs.v1.jobs.delete(
            "jobId",
        )
        assert_matches_type(JobDeleteResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.jobs.v1.jobs.with_raw_response.delete(
            "jobId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        job = await response.parse()
        assert_matches_type(JobDeleteResponse, job, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.jobs.v1.jobs.with_streaming_response.delete(
            "jobId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            job = await response.parse()
            assert_matches_type(JobDeleteResponse, job, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `job_id` but received ''"):
            await async_client.jobs.v1.jobs.with_raw_response.delete(
                "",
            )
