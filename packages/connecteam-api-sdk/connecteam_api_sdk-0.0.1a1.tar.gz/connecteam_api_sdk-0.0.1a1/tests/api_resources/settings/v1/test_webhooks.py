# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from connecteam_api_sdk import ConnecteamAPISDK, AsyncConnecteamAPISDK
from connecteam_api_sdk.types.settings.v1 import (
    WebhookListResponse,
    WebhookDeleteResponse,
    PublicBaseWebhookResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestWebhooks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: ConnecteamAPISDK) -> None:
        webhook = client.settings.v1.webhooks.create(
            event_types=["string"],
            feature_type="featureType",
            name="name",
            url="https://example.com",
        )
        assert_matches_type(PublicBaseWebhookResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: ConnecteamAPISDK) -> None:
        webhook = client.settings.v1.webhooks.create(
            event_types=["string"],
            feature_type="featureType",
            name="name",
            url="https://example.com",
            is_disabled=True,
            object_id=0,
            secret_key="secretKey",
        )
        assert_matches_type(PublicBaseWebhookResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: ConnecteamAPISDK) -> None:
        response = client.settings.v1.webhooks.with_raw_response.create(
            event_types=["string"],
            feature_type="featureType",
            name="name",
            url="https://example.com",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = response.parse()
        assert_matches_type(PublicBaseWebhookResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: ConnecteamAPISDK) -> None:
        with client.settings.v1.webhooks.with_streaming_response.create(
            event_types=["string"],
            feature_type="featureType",
            name="name",
            url="https://example.com",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = response.parse()
            assert_matches_type(PublicBaseWebhookResponse, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: ConnecteamAPISDK) -> None:
        webhook = client.settings.v1.webhooks.retrieve(
            0,
        )
        assert_matches_type(PublicBaseWebhookResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: ConnecteamAPISDK) -> None:
        response = client.settings.v1.webhooks.with_raw_response.retrieve(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = response.parse()
        assert_matches_type(PublicBaseWebhookResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: ConnecteamAPISDK) -> None:
        with client.settings.v1.webhooks.with_streaming_response.retrieve(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = response.parse()
            assert_matches_type(PublicBaseWebhookResponse, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: ConnecteamAPISDK) -> None:
        webhook = client.settings.v1.webhooks.update(
            webhook_id=0,
        )
        assert_matches_type(PublicBaseWebhookResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: ConnecteamAPISDK) -> None:
        webhook = client.settings.v1.webhooks.update(
            webhook_id=0,
            event_types=["string"],
            feature_type="featureType",
            is_disabled=True,
            name="name",
            object_id=0,
            secret_key="secretKey",
            url="https://example.com",
        )
        assert_matches_type(PublicBaseWebhookResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: ConnecteamAPISDK) -> None:
        response = client.settings.v1.webhooks.with_raw_response.update(
            webhook_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = response.parse()
        assert_matches_type(PublicBaseWebhookResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: ConnecteamAPISDK) -> None:
        with client.settings.v1.webhooks.with_streaming_response.update(
            webhook_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = response.parse()
            assert_matches_type(PublicBaseWebhookResponse, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: ConnecteamAPISDK) -> None:
        webhook = client.settings.v1.webhooks.list()
        assert_matches_type(WebhookListResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: ConnecteamAPISDK) -> None:
        webhook = client.settings.v1.webhooks.list(
            feature_type="featureType",
            limit=1,
            offset=0,
        )
        assert_matches_type(WebhookListResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: ConnecteamAPISDK) -> None:
        response = client.settings.v1.webhooks.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = response.parse()
        assert_matches_type(WebhookListResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: ConnecteamAPISDK) -> None:
        with client.settings.v1.webhooks.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = response.parse()
            assert_matches_type(WebhookListResponse, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: ConnecteamAPISDK) -> None:
        webhook = client.settings.v1.webhooks.delete(
            0,
        )
        assert_matches_type(WebhookDeleteResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: ConnecteamAPISDK) -> None:
        response = client.settings.v1.webhooks.with_raw_response.delete(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = response.parse()
        assert_matches_type(WebhookDeleteResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: ConnecteamAPISDK) -> None:
        with client.settings.v1.webhooks.with_streaming_response.delete(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = response.parse()
            assert_matches_type(WebhookDeleteResponse, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncWebhooks:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncConnecteamAPISDK) -> None:
        webhook = await async_client.settings.v1.webhooks.create(
            event_types=["string"],
            feature_type="featureType",
            name="name",
            url="https://example.com",
        )
        assert_matches_type(PublicBaseWebhookResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        webhook = await async_client.settings.v1.webhooks.create(
            event_types=["string"],
            feature_type="featureType",
            name="name",
            url="https://example.com",
            is_disabled=True,
            object_id=0,
            secret_key="secretKey",
        )
        assert_matches_type(PublicBaseWebhookResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.settings.v1.webhooks.with_raw_response.create(
            event_types=["string"],
            feature_type="featureType",
            name="name",
            url="https://example.com",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = await response.parse()
        assert_matches_type(PublicBaseWebhookResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.settings.v1.webhooks.with_streaming_response.create(
            event_types=["string"],
            feature_type="featureType",
            name="name",
            url="https://example.com",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = await response.parse()
            assert_matches_type(PublicBaseWebhookResponse, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncConnecteamAPISDK) -> None:
        webhook = await async_client.settings.v1.webhooks.retrieve(
            0,
        )
        assert_matches_type(PublicBaseWebhookResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.settings.v1.webhooks.with_raw_response.retrieve(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = await response.parse()
        assert_matches_type(PublicBaseWebhookResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.settings.v1.webhooks.with_streaming_response.retrieve(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = await response.parse()
            assert_matches_type(PublicBaseWebhookResponse, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        webhook = await async_client.settings.v1.webhooks.update(
            webhook_id=0,
        )
        assert_matches_type(PublicBaseWebhookResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        webhook = await async_client.settings.v1.webhooks.update(
            webhook_id=0,
            event_types=["string"],
            feature_type="featureType",
            is_disabled=True,
            name="name",
            object_id=0,
            secret_key="secretKey",
            url="https://example.com",
        )
        assert_matches_type(PublicBaseWebhookResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.settings.v1.webhooks.with_raw_response.update(
            webhook_id=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = await response.parse()
        assert_matches_type(PublicBaseWebhookResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.settings.v1.webhooks.with_streaming_response.update(
            webhook_id=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = await response.parse()
            assert_matches_type(PublicBaseWebhookResponse, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        webhook = await async_client.settings.v1.webhooks.list()
        assert_matches_type(WebhookListResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        webhook = await async_client.settings.v1.webhooks.list(
            feature_type="featureType",
            limit=1,
            offset=0,
        )
        assert_matches_type(WebhookListResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.settings.v1.webhooks.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = await response.parse()
        assert_matches_type(WebhookListResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.settings.v1.webhooks.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = await response.parse()
            assert_matches_type(WebhookListResponse, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncConnecteamAPISDK) -> None:
        webhook = await async_client.settings.v1.webhooks.delete(
            0,
        )
        assert_matches_type(WebhookDeleteResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.settings.v1.webhooks.with_raw_response.delete(
            0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        webhook = await response.parse()
        assert_matches_type(WebhookDeleteResponse, webhook, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.settings.v1.webhooks.with_streaming_response.delete(
            0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            webhook = await response.parse()
            assert_matches_type(WebhookDeleteResponse, webhook, path=["response"])

        assert cast(Any, response.is_closed) is True
