# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Union, Mapping
from typing_extensions import Self, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    NOT_GIVEN,
    Omit,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._utils import is_given, get_async_library
from ._version import __version__
from .resources import me
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError, ConnecteamApisdkError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)
from .resources.chat import chat
from .resources.jobs import jobs
from .resources.forms import forms
from .resources.tasks import tasks
from .resources.users import users
from .resources.settings import settings
from .resources.time_off import time_off
from .resources.scheduler import scheduler
from .resources.daily_info import daily_info
from .resources.publishers import publishers
from .resources.time_clock import time_clock
from .resources.attachments import attachments

__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "ConnecteamAPISDK",
    "AsyncConnecteamAPISDK",
    "Client",
    "AsyncClient",
]


class ConnecteamAPISDK(SyncAPIClient):
    me: me.MeResource
    settings: settings.SettingsResource
    attachments: attachments.AttachmentsResource
    forms: forms.FormsResource
    scheduler: scheduler.SchedulerResource
    jobs: jobs.JobsResource
    users: users.UsersResource
    time_off: time_off.TimeOffResource
    time_clock: time_clock.TimeClockResource
    tasks: tasks.TasksResource
    daily_info: daily_info.DailyInfoResource
    chat: chat.ChatResource
    publishers: publishers.PublishersResource
    with_raw_response: ConnecteamAPISDKWithRawResponse
    with_streaming_response: ConnecteamAPISDKWithStreamedResponse

    # client options
    api_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous ConnecteamAPISDK client instance.

        This automatically infers the `api_key` argument from the `CONNECTEAM_API_SDK_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("CONNECTEAM_API_SDK_API_KEY")
        if api_key is None:
            raise ConnecteamApisdkError(
                "The api_key client option must be set either by passing api_key to the client or by setting the CONNECTEAM_API_SDK_API_KEY environment variable"
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("CONNECTEAM_API_SDK_BASE_URL")
        if base_url is None:
            base_url = f"https://api.connecteam.com/"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.me = me.MeResource(self)
        self.settings = settings.SettingsResource(self)
        self.attachments = attachments.AttachmentsResource(self)
        self.forms = forms.FormsResource(self)
        self.scheduler = scheduler.SchedulerResource(self)
        self.jobs = jobs.JobsResource(self)
        self.users = users.UsersResource(self)
        self.time_off = time_off.TimeOffResource(self)
        self.time_clock = time_clock.TimeClockResource(self)
        self.tasks = tasks.TasksResource(self)
        self.daily_info = daily_info.DailyInfoResource(self)
        self.chat = chat.ChatResource(self)
        self.publishers = publishers.PublishersResource(self)
        self.with_raw_response = ConnecteamAPISDKWithRawResponse(self)
        self.with_streaming_response = ConnecteamAPISDKWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"X-API-KEY": api_key}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncConnecteamAPISDK(AsyncAPIClient):
    me: me.AsyncMeResource
    settings: settings.AsyncSettingsResource
    attachments: attachments.AsyncAttachmentsResource
    forms: forms.AsyncFormsResource
    scheduler: scheduler.AsyncSchedulerResource
    jobs: jobs.AsyncJobsResource
    users: users.AsyncUsersResource
    time_off: time_off.AsyncTimeOffResource
    time_clock: time_clock.AsyncTimeClockResource
    tasks: tasks.AsyncTasksResource
    daily_info: daily_info.AsyncDailyInfoResource
    chat: chat.AsyncChatResource
    publishers: publishers.AsyncPublishersResource
    with_raw_response: AsyncConnecteamAPISDKWithRawResponse
    with_streaming_response: AsyncConnecteamAPISDKWithStreamedResponse

    # client options
    api_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async AsyncConnecteamAPISDK client instance.

        This automatically infers the `api_key` argument from the `CONNECTEAM_API_SDK_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("CONNECTEAM_API_SDK_API_KEY")
        if api_key is None:
            raise ConnecteamApisdkError(
                "The api_key client option must be set either by passing api_key to the client or by setting the CONNECTEAM_API_SDK_API_KEY environment variable"
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("CONNECTEAM_API_SDK_BASE_URL")
        if base_url is None:
            base_url = f"https://api.connecteam.com/"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.me = me.AsyncMeResource(self)
        self.settings = settings.AsyncSettingsResource(self)
        self.attachments = attachments.AsyncAttachmentsResource(self)
        self.forms = forms.AsyncFormsResource(self)
        self.scheduler = scheduler.AsyncSchedulerResource(self)
        self.jobs = jobs.AsyncJobsResource(self)
        self.users = users.AsyncUsersResource(self)
        self.time_off = time_off.AsyncTimeOffResource(self)
        self.time_clock = time_clock.AsyncTimeClockResource(self)
        self.tasks = tasks.AsyncTasksResource(self)
        self.daily_info = daily_info.AsyncDailyInfoResource(self)
        self.chat = chat.AsyncChatResource(self)
        self.publishers = publishers.AsyncPublishersResource(self)
        self.with_raw_response = AsyncConnecteamAPISDKWithRawResponse(self)
        self.with_streaming_response = AsyncConnecteamAPISDKWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"X-API-KEY": api_key}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class ConnecteamAPISDKWithRawResponse:
    def __init__(self, client: ConnecteamAPISDK) -> None:
        self.me = me.MeResourceWithRawResponse(client.me)
        self.settings = settings.SettingsResourceWithRawResponse(client.settings)
        self.attachments = attachments.AttachmentsResourceWithRawResponse(client.attachments)
        self.forms = forms.FormsResourceWithRawResponse(client.forms)
        self.scheduler = scheduler.SchedulerResourceWithRawResponse(client.scheduler)
        self.jobs = jobs.JobsResourceWithRawResponse(client.jobs)
        self.users = users.UsersResourceWithRawResponse(client.users)
        self.time_off = time_off.TimeOffResourceWithRawResponse(client.time_off)
        self.time_clock = time_clock.TimeClockResourceWithRawResponse(client.time_clock)
        self.tasks = tasks.TasksResourceWithRawResponse(client.tasks)
        self.daily_info = daily_info.DailyInfoResourceWithRawResponse(client.daily_info)
        self.chat = chat.ChatResourceWithRawResponse(client.chat)
        self.publishers = publishers.PublishersResourceWithRawResponse(client.publishers)


class AsyncConnecteamAPISDKWithRawResponse:
    def __init__(self, client: AsyncConnecteamAPISDK) -> None:
        self.me = me.AsyncMeResourceWithRawResponse(client.me)
        self.settings = settings.AsyncSettingsResourceWithRawResponse(client.settings)
        self.attachments = attachments.AsyncAttachmentsResourceWithRawResponse(client.attachments)
        self.forms = forms.AsyncFormsResourceWithRawResponse(client.forms)
        self.scheduler = scheduler.AsyncSchedulerResourceWithRawResponse(client.scheduler)
        self.jobs = jobs.AsyncJobsResourceWithRawResponse(client.jobs)
        self.users = users.AsyncUsersResourceWithRawResponse(client.users)
        self.time_off = time_off.AsyncTimeOffResourceWithRawResponse(client.time_off)
        self.time_clock = time_clock.AsyncTimeClockResourceWithRawResponse(client.time_clock)
        self.tasks = tasks.AsyncTasksResourceWithRawResponse(client.tasks)
        self.daily_info = daily_info.AsyncDailyInfoResourceWithRawResponse(client.daily_info)
        self.chat = chat.AsyncChatResourceWithRawResponse(client.chat)
        self.publishers = publishers.AsyncPublishersResourceWithRawResponse(client.publishers)


class ConnecteamAPISDKWithStreamedResponse:
    def __init__(self, client: ConnecteamAPISDK) -> None:
        self.me = me.MeResourceWithStreamingResponse(client.me)
        self.settings = settings.SettingsResourceWithStreamingResponse(client.settings)
        self.attachments = attachments.AttachmentsResourceWithStreamingResponse(client.attachments)
        self.forms = forms.FormsResourceWithStreamingResponse(client.forms)
        self.scheduler = scheduler.SchedulerResourceWithStreamingResponse(client.scheduler)
        self.jobs = jobs.JobsResourceWithStreamingResponse(client.jobs)
        self.users = users.UsersResourceWithStreamingResponse(client.users)
        self.time_off = time_off.TimeOffResourceWithStreamingResponse(client.time_off)
        self.time_clock = time_clock.TimeClockResourceWithStreamingResponse(client.time_clock)
        self.tasks = tasks.TasksResourceWithStreamingResponse(client.tasks)
        self.daily_info = daily_info.DailyInfoResourceWithStreamingResponse(client.daily_info)
        self.chat = chat.ChatResourceWithStreamingResponse(client.chat)
        self.publishers = publishers.PublishersResourceWithStreamingResponse(client.publishers)


class AsyncConnecteamAPISDKWithStreamedResponse:
    def __init__(self, client: AsyncConnecteamAPISDK) -> None:
        self.me = me.AsyncMeResourceWithStreamingResponse(client.me)
        self.settings = settings.AsyncSettingsResourceWithStreamingResponse(client.settings)
        self.attachments = attachments.AsyncAttachmentsResourceWithStreamingResponse(client.attachments)
        self.forms = forms.AsyncFormsResourceWithStreamingResponse(client.forms)
        self.scheduler = scheduler.AsyncSchedulerResourceWithStreamingResponse(client.scheduler)
        self.jobs = jobs.AsyncJobsResourceWithStreamingResponse(client.jobs)
        self.users = users.AsyncUsersResourceWithStreamingResponse(client.users)
        self.time_off = time_off.AsyncTimeOffResourceWithStreamingResponse(client.time_off)
        self.time_clock = time_clock.AsyncTimeClockResourceWithStreamingResponse(client.time_clock)
        self.tasks = tasks.AsyncTasksResourceWithStreamingResponse(client.tasks)
        self.daily_info = daily_info.AsyncDailyInfoResourceWithStreamingResponse(client.daily_info)
        self.chat = chat.AsyncChatResourceWithStreamingResponse(client.chat)
        self.publishers = publishers.AsyncPublishersResourceWithStreamingResponse(client.publishers)


Client = ConnecteamAPISDK

AsyncClient = AsyncConnecteamAPISDK
