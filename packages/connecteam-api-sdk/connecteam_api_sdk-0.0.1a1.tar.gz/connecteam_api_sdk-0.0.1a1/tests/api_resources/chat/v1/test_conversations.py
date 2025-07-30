# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from connecteam_api_sdk import ConnecteamAPISDK, AsyncConnecteamAPISDK
from connecteam_api_sdk.types.chat.v1 import (
    ConversationListResponse,
)
from connecteam_api_sdk.types.users.v1.custom_fields import APIResponseBase

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestConversations:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: ConnecteamAPISDK) -> None:
        conversation = client.chat.v1.conversations.list()
        assert_matches_type(ConversationListResponse, conversation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: ConnecteamAPISDK) -> None:
        conversation = client.chat.v1.conversations.list(
            limit=1,
            offset=0,
        )
        assert_matches_type(ConversationListResponse, conversation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: ConnecteamAPISDK) -> None:
        response = client.chat.v1.conversations.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        conversation = response.parse()
        assert_matches_type(ConversationListResponse, conversation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: ConnecteamAPISDK) -> None:
        with client.chat.v1.conversations.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            conversation = response.parse()
            assert_matches_type(ConversationListResponse, conversation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_send_message(self, client: ConnecteamAPISDK) -> None:
        conversation = client.chat.v1.conversations.send_message(
            conversation_id="conversationId",
            sender_id=0,
            text="text",
        )
        assert_matches_type(APIResponseBase, conversation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_send_message_with_all_params(self, client: ConnecteamAPISDK) -> None:
        conversation = client.chat.v1.conversations.send_message(
            conversation_id="conversationId",
            sender_id=0,
            text="text",
            attachments=[
                {
                    "file_id": "fileId",
                    "type": "image",
                }
            ],
        )
        assert_matches_type(APIResponseBase, conversation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_send_message(self, client: ConnecteamAPISDK) -> None:
        response = client.chat.v1.conversations.with_raw_response.send_message(
            conversation_id="conversationId",
            sender_id=0,
            text="text",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        conversation = response.parse()
        assert_matches_type(APIResponseBase, conversation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_send_message(self, client: ConnecteamAPISDK) -> None:
        with client.chat.v1.conversations.with_streaming_response.send_message(
            conversation_id="conversationId",
            sender_id=0,
            text="text",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            conversation = response.parse()
            assert_matches_type(APIResponseBase, conversation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_send_message(self, client: ConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `conversation_id` but received ''"):
            client.chat.v1.conversations.with_raw_response.send_message(
                conversation_id="",
                sender_id=0,
                text="text",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_send_private_message(self, client: ConnecteamAPISDK) -> None:
        conversation = client.chat.v1.conversations.send_private_message(
            user_id=0,
            sender_id=0,
            text="text",
        )
        assert_matches_type(APIResponseBase, conversation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_send_private_message_with_all_params(self, client: ConnecteamAPISDK) -> None:
        conversation = client.chat.v1.conversations.send_private_message(
            user_id=0,
            sender_id=0,
            text="text",
            attachments=[
                {
                    "file_id": "fileId",
                    "type": "image",
                }
            ],
        )
        assert_matches_type(APIResponseBase, conversation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_send_private_message(self, client: ConnecteamAPISDK) -> None:
        response = client.chat.v1.conversations.with_raw_response.send_private_message(
            user_id=0,
            sender_id=0,
            text="text",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        conversation = response.parse()
        assert_matches_type(APIResponseBase, conversation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_send_private_message(self, client: ConnecteamAPISDK) -> None:
        with client.chat.v1.conversations.with_streaming_response.send_private_message(
            user_id=0,
            sender_id=0,
            text="text",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            conversation = response.parse()
            assert_matches_type(APIResponseBase, conversation, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncConversations:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        conversation = await async_client.chat.v1.conversations.list()
        assert_matches_type(ConversationListResponse, conversation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        conversation = await async_client.chat.v1.conversations.list(
            limit=1,
            offset=0,
        )
        assert_matches_type(ConversationListResponse, conversation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.chat.v1.conversations.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        conversation = await response.parse()
        assert_matches_type(ConversationListResponse, conversation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.chat.v1.conversations.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            conversation = await response.parse()
            assert_matches_type(ConversationListResponse, conversation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_send_message(self, async_client: AsyncConnecteamAPISDK) -> None:
        conversation = await async_client.chat.v1.conversations.send_message(
            conversation_id="conversationId",
            sender_id=0,
            text="text",
        )
        assert_matches_type(APIResponseBase, conversation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_send_message_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        conversation = await async_client.chat.v1.conversations.send_message(
            conversation_id="conversationId",
            sender_id=0,
            text="text",
            attachments=[
                {
                    "file_id": "fileId",
                    "type": "image",
                }
            ],
        )
        assert_matches_type(APIResponseBase, conversation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_send_message(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.chat.v1.conversations.with_raw_response.send_message(
            conversation_id="conversationId",
            sender_id=0,
            text="text",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        conversation = await response.parse()
        assert_matches_type(APIResponseBase, conversation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_send_message(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.chat.v1.conversations.with_streaming_response.send_message(
            conversation_id="conversationId",
            sender_id=0,
            text="text",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            conversation = await response.parse()
            assert_matches_type(APIResponseBase, conversation, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_send_message(self, async_client: AsyncConnecteamAPISDK) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `conversation_id` but received ''"):
            await async_client.chat.v1.conversations.with_raw_response.send_message(
                conversation_id="",
                sender_id=0,
                text="text",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_send_private_message(self, async_client: AsyncConnecteamAPISDK) -> None:
        conversation = await async_client.chat.v1.conversations.send_private_message(
            user_id=0,
            sender_id=0,
            text="text",
        )
        assert_matches_type(APIResponseBase, conversation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_send_private_message_with_all_params(self, async_client: AsyncConnecteamAPISDK) -> None:
        conversation = await async_client.chat.v1.conversations.send_private_message(
            user_id=0,
            sender_id=0,
            text="text",
            attachments=[
                {
                    "file_id": "fileId",
                    "type": "image",
                }
            ],
        )
        assert_matches_type(APIResponseBase, conversation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_send_private_message(self, async_client: AsyncConnecteamAPISDK) -> None:
        response = await async_client.chat.v1.conversations.with_raw_response.send_private_message(
            user_id=0,
            sender_id=0,
            text="text",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        conversation = await response.parse()
        assert_matches_type(APIResponseBase, conversation, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_send_private_message(self, async_client: AsyncConnecteamAPISDK) -> None:
        async with async_client.chat.v1.conversations.with_streaming_response.send_private_message(
            user_id=0,
            sender_id=0,
            text="text",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            conversation = await response.parse()
            assert_matches_type(APIResponseBase, conversation, path=["response"])

        assert cast(Any, response.is_closed) is True
