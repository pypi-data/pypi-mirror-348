# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal

import httpx

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
from .....types.tasks.v1.taskboards import (
    TaskType,
    TaskStatus,
    task_list_params,
    task_create_params,
    task_update_params,
)
from .....types.tasks.v1.taskboards.task_type import TaskType
from .....types.tasks.v1.taskboards.task_status import TaskStatus
from .....types.tasks.v1.taskboards.task_list_response import TaskListResponse
from .....types.tasks.v1.taskboards.task_create_response import TaskCreateResponse
from .....types.tasks.v1.taskboards.task_delete_response import TaskDeleteResponse
from .....types.tasks.v1.taskboards.task_update_response import TaskUpdateResponse
from .....types.tasks.v1.taskboards.task_description_param import TaskDescriptionParam

__all__ = ["TasksResource", "AsyncTasksResource"]


class TasksResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TasksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return TasksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TasksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return TasksResourceWithStreamingResponse(self)

    def create(
        self,
        task_board_id: str,
        *,
        due_date: int,
        start_time: int,
        status: TaskStatus,
        title: str,
        user_ids: Iterable[int],
        description: TaskDescriptionParam | NotGiven = NOT_GIVEN,
        is_archived: bool | NotGiven = NOT_GIVEN,
        label_ids: List[str] | NotGiven = NOT_GIVEN,
        type: TaskType | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TaskCreateResponse:
        """
        Create quick task for specified users by their ID, detailing information such as
        title, due date and description.

        Args:
          task_board_id: The unique identifier of the taskBoard

          due_date: The due date of the task in Unix format (in seconds)

          start_time: The start time of the task in Unix format (in seconds)

          status: An enumeration.

          title: The title of the task

          user_ids: List of user IDs to assign the task to. If more than one user ID is specified,
              it will be treated as a group task. To assign the task to multiple users
              individually, separate the requests. If this field remains empty the status
              field must be 'draft' and not archived.

          description: Specifies additional description on the task

          is_archived: Indicates if the task is archived

          label_ids: List of labels IDs associated with the task

          type: An enumeration.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not task_board_id:
            raise ValueError(f"Expected a non-empty value for `task_board_id` but received {task_board_id!r}")
        return self._post(
            f"/tasks/v1/taskboards/{task_board_id}/tasks",
            body=maybe_transform(
                {
                    "due_date": due_date,
                    "start_time": start_time,
                    "status": status,
                    "title": title,
                    "user_ids": user_ids,
                    "description": description,
                    "is_archived": is_archived,
                    "label_ids": label_ids,
                    "type": type,
                },
                task_create_params.TaskCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TaskCreateResponse,
        )

    def update(
        self,
        task_id: str,
        *,
        task_board_id: str,
        due_date: int,
        start_time: int,
        status: TaskStatus,
        title: str,
        user_ids: Iterable[int],
        is_archived: bool | NotGiven = NOT_GIVEN,
        label_ids: List[str] | NotGiven = NOT_GIVEN,
        type: TaskType | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TaskUpdateResponse:
        """
        Update a quick task under a specified task board

        Args:
          task_board_id: The unique identifier of the taskBoard

          task_id: The unique identifier of the task.

          due_date: The due date of the task in Unix format (in seconds)

          start_time: The start time of the task in Unix format (in seconds)

          status: An enumeration.

          title: The title of the task

          user_ids: List of user IDs to assign the task to. If more than one user ID is specified,
              it will be treated as a group task. To assign the task to multiple users
              individually, separate the requests. If this field remains empty the status
              field must be 'draft' and not archived.

          is_archived: Indicates if the task is archived

          label_ids: List of labels IDs associated with the task

          type: An enumeration.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not task_board_id:
            raise ValueError(f"Expected a non-empty value for `task_board_id` but received {task_board_id!r}")
        if not task_id:
            raise ValueError(f"Expected a non-empty value for `task_id` but received {task_id!r}")
        return self._put(
            f"/tasks/v1/taskboards/{task_board_id}/tasks/{task_id}",
            body=maybe_transform(
                {
                    "due_date": due_date,
                    "start_time": start_time,
                    "status": status,
                    "title": title,
                    "user_ids": user_ids,
                    "is_archived": is_archived,
                    "label_ids": label_ids,
                    "type": type,
                },
                task_update_params.TaskUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TaskUpdateResponse,
        )

    def list(
        self,
        task_board_id: str,
        *,
        label_ids: List[str] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        status: Literal["draft", "published", "completed", "all"] | NotGiven = NOT_GIVEN,
        task_ids: List[str] | NotGiven = NOT_GIVEN,
        user_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TaskListResponse:
        """
        Retrieves a list of tasks under a specified task board

        Args:
          task_board_id: The unique identifier of the taskBoard

          label_ids: List of label IDs to filter by. Tasks retrieved will include the specified
              label(s), but may also include additional labels.

          limit: The maximum number of results to display per page

          offset: The resource offset of the last successfully read resource will be returned as
              the paging.offset JSON property of a paginated response containing more results

          status: An enumeration.

          task_ids: List of task IDs to filter by

          user_ids: List of assigned user IDs on the task to filter by. Group tasks will be also
              included in the results.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not task_board_id:
            raise ValueError(f"Expected a non-empty value for `task_board_id` but received {task_board_id!r}")
        return self._get(
            f"/tasks/v1/taskboards/{task_board_id}/tasks",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "label_ids": label_ids,
                        "limit": limit,
                        "offset": offset,
                        "status": status,
                        "task_ids": task_ids,
                        "user_ids": user_ids,
                    },
                    task_list_params.TaskListParams,
                ),
            ),
            cast_to=TaskListResponse,
        )

    def delete(
        self,
        task_id: str,
        *,
        task_board_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TaskDeleteResponse:
        """
        Delete quick task under a specified task board

        Args:
          task_board_id: The unique identifier of the taskBoard

          task_id: The unique identifier of the task

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not task_board_id:
            raise ValueError(f"Expected a non-empty value for `task_board_id` but received {task_board_id!r}")
        if not task_id:
            raise ValueError(f"Expected a non-empty value for `task_id` but received {task_id!r}")
        return self._delete(
            f"/tasks/v1/taskboards/{task_board_id}/tasks/{task_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TaskDeleteResponse,
        )


class AsyncTasksResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTasksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTasksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTasksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return AsyncTasksResourceWithStreamingResponse(self)

    async def create(
        self,
        task_board_id: str,
        *,
        due_date: int,
        start_time: int,
        status: TaskStatus,
        title: str,
        user_ids: Iterable[int],
        description: TaskDescriptionParam | NotGiven = NOT_GIVEN,
        is_archived: bool | NotGiven = NOT_GIVEN,
        label_ids: List[str] | NotGiven = NOT_GIVEN,
        type: TaskType | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TaskCreateResponse:
        """
        Create quick task for specified users by their ID, detailing information such as
        title, due date and description.

        Args:
          task_board_id: The unique identifier of the taskBoard

          due_date: The due date of the task in Unix format (in seconds)

          start_time: The start time of the task in Unix format (in seconds)

          status: An enumeration.

          title: The title of the task

          user_ids: List of user IDs to assign the task to. If more than one user ID is specified,
              it will be treated as a group task. To assign the task to multiple users
              individually, separate the requests. If this field remains empty the status
              field must be 'draft' and not archived.

          description: Specifies additional description on the task

          is_archived: Indicates if the task is archived

          label_ids: List of labels IDs associated with the task

          type: An enumeration.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not task_board_id:
            raise ValueError(f"Expected a non-empty value for `task_board_id` but received {task_board_id!r}")
        return await self._post(
            f"/tasks/v1/taskboards/{task_board_id}/tasks",
            body=await async_maybe_transform(
                {
                    "due_date": due_date,
                    "start_time": start_time,
                    "status": status,
                    "title": title,
                    "user_ids": user_ids,
                    "description": description,
                    "is_archived": is_archived,
                    "label_ids": label_ids,
                    "type": type,
                },
                task_create_params.TaskCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TaskCreateResponse,
        )

    async def update(
        self,
        task_id: str,
        *,
        task_board_id: str,
        due_date: int,
        start_time: int,
        status: TaskStatus,
        title: str,
        user_ids: Iterable[int],
        is_archived: bool | NotGiven = NOT_GIVEN,
        label_ids: List[str] | NotGiven = NOT_GIVEN,
        type: TaskType | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TaskUpdateResponse:
        """
        Update a quick task under a specified task board

        Args:
          task_board_id: The unique identifier of the taskBoard

          task_id: The unique identifier of the task.

          due_date: The due date of the task in Unix format (in seconds)

          start_time: The start time of the task in Unix format (in seconds)

          status: An enumeration.

          title: The title of the task

          user_ids: List of user IDs to assign the task to. If more than one user ID is specified,
              it will be treated as a group task. To assign the task to multiple users
              individually, separate the requests. If this field remains empty the status
              field must be 'draft' and not archived.

          is_archived: Indicates if the task is archived

          label_ids: List of labels IDs associated with the task

          type: An enumeration.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not task_board_id:
            raise ValueError(f"Expected a non-empty value for `task_board_id` but received {task_board_id!r}")
        if not task_id:
            raise ValueError(f"Expected a non-empty value for `task_id` but received {task_id!r}")
        return await self._put(
            f"/tasks/v1/taskboards/{task_board_id}/tasks/{task_id}",
            body=await async_maybe_transform(
                {
                    "due_date": due_date,
                    "start_time": start_time,
                    "status": status,
                    "title": title,
                    "user_ids": user_ids,
                    "is_archived": is_archived,
                    "label_ids": label_ids,
                    "type": type,
                },
                task_update_params.TaskUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TaskUpdateResponse,
        )

    async def list(
        self,
        task_board_id: str,
        *,
        label_ids: List[str] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        status: Literal["draft", "published", "completed", "all"] | NotGiven = NOT_GIVEN,
        task_ids: List[str] | NotGiven = NOT_GIVEN,
        user_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TaskListResponse:
        """
        Retrieves a list of tasks under a specified task board

        Args:
          task_board_id: The unique identifier of the taskBoard

          label_ids: List of label IDs to filter by. Tasks retrieved will include the specified
              label(s), but may also include additional labels.

          limit: The maximum number of results to display per page

          offset: The resource offset of the last successfully read resource will be returned as
              the paging.offset JSON property of a paginated response containing more results

          status: An enumeration.

          task_ids: List of task IDs to filter by

          user_ids: List of assigned user IDs on the task to filter by. Group tasks will be also
              included in the results.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not task_board_id:
            raise ValueError(f"Expected a non-empty value for `task_board_id` but received {task_board_id!r}")
        return await self._get(
            f"/tasks/v1/taskboards/{task_board_id}/tasks",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "label_ids": label_ids,
                        "limit": limit,
                        "offset": offset,
                        "status": status,
                        "task_ids": task_ids,
                        "user_ids": user_ids,
                    },
                    task_list_params.TaskListParams,
                ),
            ),
            cast_to=TaskListResponse,
        )

    async def delete(
        self,
        task_id: str,
        *,
        task_board_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TaskDeleteResponse:
        """
        Delete quick task under a specified task board

        Args:
          task_board_id: The unique identifier of the taskBoard

          task_id: The unique identifier of the task

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not task_board_id:
            raise ValueError(f"Expected a non-empty value for `task_board_id` but received {task_board_id!r}")
        if not task_id:
            raise ValueError(f"Expected a non-empty value for `task_id` but received {task_id!r}")
        return await self._delete(
            f"/tasks/v1/taskboards/{task_board_id}/tasks/{task_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TaskDeleteResponse,
        )


class TasksResourceWithRawResponse:
    def __init__(self, tasks: TasksResource) -> None:
        self._tasks = tasks

        self.create = to_raw_response_wrapper(
            tasks.create,
        )
        self.update = to_raw_response_wrapper(
            tasks.update,
        )
        self.list = to_raw_response_wrapper(
            tasks.list,
        )
        self.delete = to_raw_response_wrapper(
            tasks.delete,
        )


class AsyncTasksResourceWithRawResponse:
    def __init__(self, tasks: AsyncTasksResource) -> None:
        self._tasks = tasks

        self.create = async_to_raw_response_wrapper(
            tasks.create,
        )
        self.update = async_to_raw_response_wrapper(
            tasks.update,
        )
        self.list = async_to_raw_response_wrapper(
            tasks.list,
        )
        self.delete = async_to_raw_response_wrapper(
            tasks.delete,
        )


class TasksResourceWithStreamingResponse:
    def __init__(self, tasks: TasksResource) -> None:
        self._tasks = tasks

        self.create = to_streamed_response_wrapper(
            tasks.create,
        )
        self.update = to_streamed_response_wrapper(
            tasks.update,
        )
        self.list = to_streamed_response_wrapper(
            tasks.list,
        )
        self.delete = to_streamed_response_wrapper(
            tasks.delete,
        )


class AsyncTasksResourceWithStreamingResponse:
    def __init__(self, tasks: AsyncTasksResource) -> None:
        self._tasks = tasks

        self.create = async_to_streamed_response_wrapper(
            tasks.create,
        )
        self.update = async_to_streamed_response_wrapper(
            tasks.update,
        )
        self.list = async_to_streamed_response_wrapper(
            tasks.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            tasks.delete,
        )
