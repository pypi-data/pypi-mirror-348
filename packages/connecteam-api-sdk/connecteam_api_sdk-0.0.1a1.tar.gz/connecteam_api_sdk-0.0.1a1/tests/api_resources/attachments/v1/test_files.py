# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from connecteam_api_sdk import ConnecteamAPISDK, AsyncConnecteamAPISDK
from connecteam_api_sdk.types.attachments.v1 import (
    FileRetrieveResponse,
    FileCompleteUploadResponse,
    FileGenerateUploadURLResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestFiles:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: ConnecteamAPISDK) -> None:
        file = client.attachments.v1.files.retrieve(
            "fileId",
        )
        assert_matches_type(FileRetrieveResponse, file, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: ConnecteamAPISDK) -> None:
        response = client.attachments.v1.files.with_raw_response.retrieve(
            "fileId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = response.parse()
        assert_matches_type(FileRetrieveResponse, file, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: ConnecteamAPISDK) -> None:
        with client.attachments.v1.files.with_streaming_response.retrieve(
            "fileId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = response.parse()
            assert_matches_type(FileRetrieveResponse, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: ConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `file_id` but received ''"):
            client.attachments.v1.files.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_complete_upload(self, client: ConnecteamAPISDK) -> None:
        file = client.attachments.v1.files.complete_upload(
            "fileId",
        )
        assert_matches_type(FileCompleteUploadResponse, file, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_complete_upload(self, client: ConnecteamAPISDK) -> None:
        response = client.attachments.v1.files.with_raw_response.complete_upload(
            "fileId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = response.parse()
        assert_matches_type(FileCompleteUploadResponse, file, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_complete_upload(self, client: ConnecteamAPISDK) -> None:
        with client.attachments.v1.files.with_streaming_response.complete_upload(
            "fileId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = response.parse()
            assert_matches_type(FileCompleteUploadResponse, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_complete_upload(self, client: ConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `file_id` but received ''"):
            client.attachments.v1.files.with_raw_response.complete_upload(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_generate_upload_url(self, client: ConnecteamAPISDK) -> None:
        file = client.attachments.v1.files.generate_upload_url(
            feature_type="chat",
            file_name="fileName",
        )
        assert_matches_type(FileGenerateUploadURLResponse, file, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_generate_upload_url_with_all_params(self, client: ConnecteamAPISDK) -> None:
        file = client.attachments.v1.files.generate_upload_url(
            feature_type="chat",
            file_name="fileName",
            file_type_hint="fileTypeHint",
        )
        assert_matches_type(FileGenerateUploadURLResponse, file, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_generate_upload_url(self, client: ConnecteamAPISDK) -> None:
        response = client.attachments.v1.files.with_raw_response.generate_upload_url(
            feature_type="chat",
            file_name="fileName",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = response.parse()
        assert_matches_type(FileGenerateUploadURLResponse, file, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_generate_upload_url(self, client: ConnecteamAPISDK) -> None:
        with client.attachments.v1.files.with_streaming_response.generate_upload_url(
            feature_type="chat",
            file_name="fileName",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = response.parse()
            assert_matches_type(FileGenerateUploadURLResponse, file, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncFiles:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncConnecteamAPISDK) -> None:
        file = await async_client.attachments.v1.files.retrieve(
            "fileId",
        )
        assert_matches_type(FileRetrieveResponse, file, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.attachments.v1.files.with_raw_response.retrieve(
            "fileId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = await response.parse()
        assert_matches_type(FileRetrieveResponse, file, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.attachments.v1.files.with_streaming_response.retrieve(
            "fileId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = await response.parse()
            assert_matches_type(FileRetrieveResponse, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `file_id` but received ''"):
            await async_client.attachments.v1.files.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_complete_upload(self, async_client: AsyncConnecteamAPISDK) -> None:
        file = await async_client.attachments.v1.files.complete_upload(
            "fileId",
        )
        assert_matches_type(FileCompleteUploadResponse, file, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_complete_upload(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.attachments.v1.files.with_raw_response.complete_upload(
            "fileId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = await response.parse()
        assert_matches_type(FileCompleteUploadResponse, file, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_complete_upload(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.attachments.v1.files.with_streaming_response.complete_upload(
            "fileId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = await response.parse()
            assert_matches_type(FileCompleteUploadResponse, file, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_complete_upload(self, async_client: AsyncConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `file_id` but received ''"):
            await async_client.attachments.v1.files.with_raw_response.complete_upload(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_generate_upload_url(self, async_client: AsyncConnecteamAPISDK) -> None:
        file = await async_client.attachments.v1.files.generate_upload_url(
            feature_type="chat",
            file_name="fileName",
        )
        assert_matches_type(FileGenerateUploadURLResponse, file, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_generate_upload_url_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        file = await async_client.attachments.v1.files.generate_upload_url(
            feature_type="chat",
            file_name="fileName",
            file_type_hint="fileTypeHint",
        )
        assert_matches_type(FileGenerateUploadURLResponse, file, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_generate_upload_url(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.attachments.v1.files.with_raw_response.generate_upload_url(
            feature_type="chat",
            file_name="fileName",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        file = await response.parse()
        assert_matches_type(FileGenerateUploadURLResponse, file, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_generate_upload_url(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.attachments.v1.files.with_streaming_response.generate_upload_url(
            feature_type="chat",
            file_name="fileName",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            file = await response.parse()
            assert_matches_type(FileGenerateUploadURLResponse, file, path=["response"])

        assert cast(Any, response.is_closed) is True
