# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .tasks import (
    TasksResource,
    AsyncTasksResource,
    TasksResourceWithRawResponse,
    AsyncTasksResourceWithRawResponse,
    TasksResourceWithStreamingResponse,
    AsyncTasksResourceWithStreamingResponse,
)
from ....._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ....._utils import maybe_transform, async_maybe_transform
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....._base_client import make_request_options
from .....types.tasks.v1 import taskboard_get_labels_params
from .....types.tasks.v1.taskboard_list_response import TaskboardListResponse
from .....types.tasks.v1.taskboard_get_labels_response import TaskboardGetLabelsResponse

__all__ = ["TaskboardsResource", "AsyncTaskboardsResource"]


class TaskboardsResource(SyncAPIResource):
    @cached_property
    def tasks(self) -> TasksResource:
        return TasksResource(self._client)

    @cached_property
    def with_raw_response(self) -> TaskboardsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return TaskboardsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TaskboardsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return TaskboardsResourceWithStreamingResponse(self)

    def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TaskboardListResponse:
        """Retrieve a list of task boards associated with the account"""
        return self._get(
            "/tasks/v1/taskboards",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TaskboardListResponse,
        )

    def get_labels(
        self,
        task_board_id: str,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        title: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TaskboardGetLabelsResponse:
        """
        Retrieve a list of task labels associated with the account

        Args:
          task_board_id: The unique identifier of the task board to filter by

          limit: The maximum number of results to display per page

          offset: The resource offset of the last successfully read resource will be returned as
              the paging.offset JSON property of a paginated response containing more results

          title: The title (name) of the label to filter by

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not task_board_id:
            raise ValueError(f"Expected a non-empty value for `task_board_id` but received {task_board_id!r}")
        return self._get(
            f"/tasks/v1/taskboards/{task_board_id}/labels",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                        "title": title,
                    },
                    taskboard_get_labels_params.TaskboardGetLabelsParams,
                ),
            ),
            cast_to=TaskboardGetLabelsResponse,
        )


class AsyncTaskboardsResource(AsyncAPIResource):
    @cached_property
    def tasks(self) -> AsyncTasksResource:
        return AsyncTasksResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncTaskboardsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTaskboardsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTaskboardsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return AsyncTaskboardsResourceWithStreamingResponse(self)

    async def list(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TaskboardListResponse:
        """Retrieve a list of task boards associated with the account"""
        return await self._get(
            "/tasks/v1/taskboards",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TaskboardListResponse,
        )

    async def get_labels(
        self,
        task_board_id: str,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        title: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TaskboardGetLabelsResponse:
        """
        Retrieve a list of task labels associated with the account

        Args:
          task_board_id: The unique identifier of the task board to filter by

          limit: The maximum number of results to display per page

          offset: The resource offset of the last successfully read resource will be returned as
              the paging.offset JSON property of a paginated response containing more results

          title: The title (name) of the label to filter by

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not task_board_id:
            raise ValueError(f"Expected a non-empty value for `task_board_id` but received {task_board_id!r}")
        return await self._get(
            f"/tasks/v1/taskboards/{task_board_id}/labels",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "offset": offset,
                        "title": title,
                    },
                    taskboard_get_labels_params.TaskboardGetLabelsParams,
                ),
            ),
            cast_to=TaskboardGetLabelsResponse,
        )


class TaskboardsResourceWithRawResponse:
    def __init__(self, taskboards: TaskboardsResource) -> None:
        self._taskboards = taskboards

        self.list = to_raw_response_wrapper(
            taskboards.list,
        )
        self.get_labels = to_raw_response_wrapper(
            taskboards.get_labels,
        )

    @cached_property
    def tasks(self) -> TasksResourceWithRawResponse:
        return TasksResourceWithRawResponse(self._taskboards.tasks)


class AsyncTaskboardsResourceWithRawResponse:
    def __init__(self, taskboards: AsyncTaskboardsResource) -> None:
        self._taskboards = taskboards

        self.list = async_to_raw_response_wrapper(
            taskboards.list,
        )
        self.get_labels = async_to_raw_response_wrapper(
            taskboards.get_labels,
        )

    @cached_property
    def tasks(self) -> AsyncTasksResourceWithRawResponse:
        return AsyncTasksResourceWithRawResponse(self._taskboards.tasks)


class TaskboardsResourceWithStreamingResponse:
    def __init__(self, taskboards: TaskboardsResource) -> None:
        self._taskboards = taskboards

        self.list = to_streamed_response_wrapper(
            taskboards.list,
        )
        self.get_labels = to_streamed_response_wrapper(
            taskboards.get_labels,
        )

    @cached_property
    def tasks(self) -> TasksResourceWithStreamingResponse:
        return TasksResourceWithStreamingResponse(self._taskboards.tasks)


class AsyncTaskboardsResourceWithStreamingResponse:
    def __init__(self, taskboards: AsyncTaskboardsResource) -> None:
        self._taskboards = taskboards

        self.list = async_to_streamed_response_wrapper(
            taskboards.list,
        )
        self.get_labels = async_to_streamed_response_wrapper(
            taskboards.get_labels,
        )

    @cached_property
    def tasks(self) -> AsyncTasksResourceWithStreamingResponse:
        return AsyncTasksResourceWithStreamingResponse(self._taskboards.tasks)
