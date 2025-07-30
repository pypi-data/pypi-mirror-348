# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from connecteam_api_sdk import ConnecteamAPISDK, AsyncConnecteamAPISDK
from connecteam_api_sdk.types.forms.v1.forms import (
    FormSubmissionListResponse,
    FormSubmissionUpdateResponse,
    FormSubmissionRetrieveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFormSubmissions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: ConnecteamAPISDK) -> None:
        form_submission = client.forms.v1.forms.form_submissions.retrieve(
            form_submission_id="formSubmissionId",
            form_id=0,
        )
        assert_matches_type(FormSubmissionRetrieveResponse, form_submission, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: ConnecteamAPISDK) -> None:
        response = client.forms.v1.forms.form_submissions.with_raw_response.retrieve(
            form_submission_id="formSubmissionId",
            form_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        form_submission = response.parse()
        assert_matches_type(FormSubmissionRetrieveResponse, form_submission, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: ConnecteamAPISDK) -> None:
        with client.forms.v1.forms.form_submissions.with_streaming_response.retrieve(
            form_submission_id="formSubmissionId",
            form_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            form_submission = response.parse()
            assert_matches_type(FormSubmissionRetrieveResponse, form_submission, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: ConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `form_submission_id` but received ''"):
            client.forms.v1.forms.form_submissions.with_raw_response.retrieve(
                form_submission_id="",
                form_id=0,
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: ConnecteamAPISDK) -> None:
        form_submission = client.forms.v1.forms.form_submissions.update(
            form_submission_id="formSubmissionId",
            form_id=0,
            manager_fields=[
                {
                    "files": [
                        {
                            "filename": "filename",
                            "file_url": "fileUrl",
                        }
                    ],
                    "manager_field_id": "managerFieldId",
                }
            ],
        )
        assert_matches_type(FormSubmissionUpdateResponse, form_submission, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: ConnecteamAPISDK) -> None:
        response = client.forms.v1.forms.form_submissions.with_raw_response.update(
            form_submission_id="formSubmissionId",
            form_id=0,
            manager_fields=[
                {
                    "files": [
                        {
                            "filename": "filename",
                            "file_url": "fileUrl",
                        }
                    ],
                    "manager_field_id": "managerFieldId",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        form_submission = response.parse()
        assert_matches_type(FormSubmissionUpdateResponse, form_submission, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: ConnecteamAPISDK) -> None:
        with client.forms.v1.forms.form_submissions.with_streaming_response.update(
            form_submission_id="formSubmissionId",
            form_id=0,
            manager_fields=[
                {
                    "files": [
                        {
                            "filename": "filename",
                            "file_url": "fileUrl",
                        }
                    ],
                    "manager_field_id": "managerFieldId",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            form_submission = response.parse()
            assert_matches_type(FormSubmissionUpdateResponse, form_submission, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: ConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `form_submission_id` but received ''"):
            client.forms.v1.forms.form_submissions.with_raw_response.update(
                form_submission_id="",
                form_id=0,
                manager_fields=[
                    {
                        "files": [
                            {
                                "filename": "filename",
                                "file_url": "fileUrl",
                            }
                        ],
                        "manager_field_id": "managerFieldId",
                    }
                ],
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: ConnecteamAPISDK) -> None:
        form_submission = client.forms.v1.forms.form_submissions.list(
            form_id=0,
        )
        assert_matches_type(FormSubmissionListResponse, form_submission, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: ConnecteamAPISDK) -> None:
        form_submission = client.forms.v1.forms.form_submissions.list(
            form_id=0,
            limit=1,
            offset=0,
            submitting_end_time=0,
            submitting_start_timestamp=0,
            user_ids=[0],
        )
        assert_matches_type(FormSubmissionListResponse, form_submission, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: ConnecteamAPISDK) -> None:
        response = client.forms.v1.forms.form_submissions.with_raw_response.list(
            form_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        form_submission = response.parse()
        assert_matches_type(FormSubmissionListResponse, form_submission, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: ConnecteamAPISDK) -> None:
        with client.forms.v1.forms.form_submissions.with_streaming_response.list(
            form_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            form_submission = response.parse()
            assert_matches_type(FormSubmissionListResponse, form_submission, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncFormSubmissions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncConnecteamAPISDK) -> None:
        form_submission = await async_client.forms.v1.forms.form_submissions.retrieve(
            form_submission_id="formSubmissionId",
            form_id=0,
        )
        assert_matches_type(FormSubmissionRetrieveResponse, form_submission, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.forms.v1.forms.form_submissions.with_raw_response.retrieve(
            form_submission_id="formSubmissionId",
            form_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        form_submission = await response.parse()
        assert_matches_type(FormSubmissionRetrieveResponse, form_submission, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.forms.v1.forms.form_submissions.with_streaming_response.retrieve(
            form_submission_id="formSubmissionId",
            form_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            form_submission = await response.parse()
            assert_matches_type(FormSubmissionRetrieveResponse, form_submission, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `form_submission_id` but received ''"):
            await async_client.forms.v1.forms.form_submissions.with_raw_response.retrieve(
                form_submission_id="",
                form_id=0,
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        form_submission = await async_client.forms.v1.forms.form_submissions.update(
            form_submission_id="formSubmissionId",
            form_id=0,
            manager_fields=[
                {
                    "files": [
                        {
                            "filename": "filename",
                            "file_url": "fileUrl",
                        }
                    ],
                    "manager_field_id": "managerFieldId",
                }
            ],
        )
        assert_matches_type(FormSubmissionUpdateResponse, form_submission, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.forms.v1.forms.form_submissions.with_raw_response.update(
            form_submission_id="formSubmissionId",
            form_id=0,
            manager_fields=[
                {
                    "files": [
                        {
                            "filename": "filename",
                            "file_url": "fileUrl",
                        }
                    ],
                    "manager_field_id": "managerFieldId",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        form_submission = await response.parse()
        assert_matches_type(FormSubmissionUpdateResponse, form_submission, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.forms.v1.forms.form_submissions.with_streaming_response.update(
            form_submission_id="formSubmissionId",
            form_id=0,
            manager_fields=[
                {
                    "files": [
                        {
                            "filename": "filename",
                            "file_url": "fileUrl",
                        }
                    ],
                    "manager_field_id": "managerFieldId",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            form_submission = await response.parse()
            assert_matches_type(FormSubmissionUpdateResponse, form_submission, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `form_submission_id` but received ''"):
            await async_client.forms.v1.forms.form_submissions.with_raw_response.update(
                form_submission_id="",
                form_id=0,
                manager_fields=[
                    {
                        "files": [
                            {
                                "filename": "filename",
                                "file_url": "fileUrl",
                            }
                        ],
                        "manager_field_id": "managerFieldId",
                    }
                ],
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        form_submission = await async_client.forms.v1.forms.form_submissions.list(
            form_id=0,
        )
        assert_matches_type(FormSubmissionListResponse, form_submission, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        form_submission = await async_client.forms.v1.forms.form_submissions.list(
            form_id=0,
            limit=1,
            offset=0,
            submitting_end_time=0,
            submitting_start_timestamp=0,
            user_ids=[0],
        )
        assert_matches_type(FormSubmissionListResponse, form_submission, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.forms.v1.forms.form_submissions.with_raw_response.list(
            form_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        form_submission = await response.parse()
        assert_matches_type(FormSubmissionListResponse, form_submission, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.forms.v1.forms.form_submissions.with_streaming_response.list(
            form_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            form_submission = await response.parse()
            assert_matches_type(FormSubmissionListResponse, form_submission, path=["response"])

        assert cast(Any, response.is_closed) is True
