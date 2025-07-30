# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.chat.v1 import (
    conversation_list_params,
    conversation_send_message_params,
    conversation_send_private_message_params,
)
from ....types.chat.v1.conversation_list_response import ConversationListResponse
from ....types.users.v1.custom_fields.api_response_base import APIResponseBase

__all__ = ["ConversationsResource", "AsyncConversationsResource"]


class ConversationsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ConversationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return ConversationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ConversationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return ConversationsResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConversationListResponse:
        """Retrieves a list of team chats and/or channels associated with the account.

        The
        list excludes private conversations.

        Args:
          limit: The maximum number of results to display per page

          offset: The resource offset of the last successfully read resource will be returned as
              the paging.offset JSON property of a paginated response containing more results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/chat/v1/conversations",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                    },
                    conversation_list_params.ConversationListParams,
                ),
            ),
            cast_to=ConversationListResponse,
        )

    def send_message(
        self,
        conversation_id: str,
        *,
        sender_id: int,
        text: str,
        attachments: Iterable[conversation_send_message_params.Attachment] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIResponseBase:
        """
        Sends a new message to a specific chat, whether it’s channel or a team chat

        Args:
          conversation_id: The unique identifier of the conversation

          sender_id: The unique identifier of the sender (custom publisher). The custom publishers
              page can be found in the UI under Settings -> Feed settings.

          text: Specifies the text content of the message. Must be in UTF-8 and less than 500
              characters.

          attachments: List of attachments to be associated with the message.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not conversation_id:
            raise ValueError(f"Expected a non-empty value for `conversation_id` but received {conversation_id!r}")
        return self._post(
            f"/chat/v1/conversations/{conversation_id}/message",
            body=maybe_transform(
                {
                    "sender_id": sender_id,
                    "text": text,
                    "attachments": attachments,
                },
                conversation_send_message_params.ConversationSendMessageParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIResponseBase,
        )

    def send_private_message(
        self,
        user_id: int,
        *,
        sender_id: int,
        text: str,
        attachments: Iterable[conversation_send_private_message_params.Attachment] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIResponseBase:
        """Send a private message to a specified user within the account.

        The sender will
        be a custom publisher. If a conversation between the custom publisher and the
        addressed user already exists, it will send the message to the same
        conversation, if not, it will create a new conversation with the specified user.

        Args:
          user_id: The unique identifier of the user

          sender_id: The unique identifier of the sender (custom publisher). The custom publishers
              page can be found in the UI under Settings -> Feed settings.

          text: Specifies the text content of the message. Must be in UTF-8 and less than 500
              characters.

          attachments: List of attachments to be associated with the message.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            f"/chat/v1/conversations/privateMessage/{user_id}",
            body=maybe_transform(
                {
                    "sender_id": sender_id,
                    "text": text,
                    "attachments": attachments,
                },
                conversation_send_private_message_params.ConversationSendPrivateMessageParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIResponseBase,
        )


class AsyncConversationsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncConversationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncConversationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncConversationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return AsyncConversationsResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConversationListResponse:
        """Retrieves a list of team chats and/or channels associated with the account.

        The
        list excludes private conversations.

        Args:
          limit: The maximum number of results to display per page

          offset: The resource offset of the last successfully read resource will be returned as
              the paging.offset JSON property of a paginated response containing more results

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/chat/v1/conversations",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                    },
                    conversation_list_params.ConversationListParams,
                ),
            ),
            cast_to=ConversationListResponse,
        )

    async def send_message(
        self,
        conversation_id: str,
        *,
        sender_id: int,
        text: str,
        attachments: Iterable[conversation_send_message_params.Attachment] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIResponseBase:
        """
        Sends a new message to a specific chat, whether it’s channel or a team chat

        Args:
          conversation_id: The unique identifier of the conversation

          sender_id: The unique identifier of the sender (custom publisher). The custom publishers
              page can be found in the UI under Settings -> Feed settings.

          text: Specifies the text content of the message. Must be in UTF-8 and less than 500
              characters.

          attachments: List of attachments to be associated with the message.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not conversation_id:
            raise ValueError(f"Expected a non-empty value for `conversation_id` but received {conversation_id!r}")
        return await self._post(
            f"/chat/v1/conversations/{conversation_id}/message",
            body=await async_maybe_transform(
                {
                    "sender_id": sender_id,
                    "text": text,
                    "attachments": attachments,
                },
                conversation_send_message_params.ConversationSendMessageParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIResponseBase,
        )

    async def send_private_message(
        self,
        user_id: int,
        *,
        sender_id: int,
        text: str,
        attachments: Iterable[conversation_send_private_message_params.Attachment] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIResponseBase:
        """Send a private message to a specified user within the account.

        The sender will
        be a custom publisher. If a conversation between the custom publisher and the
        addressed user already exists, it will send the message to the same
        conversation, if not, it will create a new conversation with the specified user.

        Args:
          user_id: The unique identifier of the user

          sender_id: The unique identifier of the sender (custom publisher). The custom publishers
              page can be found in the UI under Settings -> Feed settings.

          text: Specifies the text content of the message. Must be in UTF-8 and less than 500
              characters.

          attachments: List of attachments to be associated with the message.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            f"/chat/v1/conversations/privateMessage/{user_id}",
            body=await async_maybe_transform(
                {
                    "sender_id": sender_id,
                    "text": text,
                    "attachments": attachments,
                },
                conversation_send_private_message_params.ConversationSendPrivateMessageParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIResponseBase,
        )


class ConversationsResourceWithRawResponse:
    def __init__(self, conversations: ConversationsResource) -> None:
        self._conversations = conversations

        self.list = to_raw_response_wrapper(
            conversations.list,
        )
        self.send_message = to_raw_response_wrapper(
            conversations.send_message,
        )
        self.send_private_message = to_raw_response_wrapper(
            conversations.send_private_message,
        )


class AsyncConversationsResourceWithRawResponse:
    def __init__(self, conversations: AsyncConversationsResource) -> None:
        self._conversations = conversations

        self.list = async_to_raw_response_wrapper(
            conversations.list,
        )
        self.send_message = async_to_raw_response_wrapper(
            conversations.send_message,
        )
        self.send_private_message = async_to_raw_response_wrapper(
            conversations.send_private_message,
        )


class ConversationsResourceWithStreamingResponse:
    def __init__(self, conversations: ConversationsResource) -> None:
        self._conversations = conversations

        self.list = to_streamed_response_wrapper(
            conversations.list,
        )
        self.send_message = to_streamed_response_wrapper(
            conversations.send_message,
        )
        self.send_private_message = to_streamed_response_wrapper(
            conversations.send_private_message,
        )


class AsyncConversationsResourceWithStreamingResponse:
    def __init__(self, conversations: AsyncConversationsResource) -> None:
        self._conversations = conversations

        self.list = async_to_streamed_response_wrapper(
            conversations.list,
        )
        self.send_message = async_to_streamed_response_wrapper(
            conversations.send_message,
        )
        self.send_private_message = async_to_streamed_response_wrapper(
            conversations.send_private_message,
        )
