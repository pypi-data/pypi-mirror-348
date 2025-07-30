# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal, overload

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import required_args, maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.jobs.v1 import job_list_params, job_create_params, job_update_params
from ....types.jobs.v1.api_response import APIResponse
from ....types.scheduler.v1.schedulers import SortOrder
from ....types.jobs.v1.job_list_response import JobListResponse
from ....types.jobs.v1.job_create_response import JobCreateResponse
from ....types.jobs.v1.job_delete_response import JobDeleteResponse
from ....types.jobs.v1.assign_data_in_param import AssignDataInParam
from ....types.time_clock.v1.gps_data_param import GpsDataParam
from ....types.scheduler.v1.schedulers.sort_order import SortOrder

__all__ = ["JobsResource", "AsyncJobsResource"]


class JobsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> JobsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return JobsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> JobsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return JobsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        body: Iterable[job_create_params.Body],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> JobCreateResponse:
        """
        Create individual or multiple jobs under a specified scheduler

        Args:
          body: Request model for the new Jobs

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/jobs/v1/jobs",
            body=maybe_transform(body, Iterable[job_create_params.Body]),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=JobCreateResponse,
        )

    def retrieve(
        self,
        job_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIResponse:
        """
        Retrieve a single job information by its unique ID

        Args:
          job_id: The unique identifier of the job

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not job_id:
            raise ValueError(f"Expected a non-empty value for `job_id` but received {job_id!r}")
        return self._get(
            f"/jobs/v1/jobs/{job_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIResponse,
        )

    @overload
    def update(
        self,
        job_id: str,
        *,
        parent_id: str,
        title: str,
        use_parent_data: bool,
        assign: AssignDataInParam | NotGiven = NOT_GIVEN,
        code: str | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        gps: GpsDataParam | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIResponse:
        """Update a single job by its unique identifier.

        Currently, updating job with
        nested sub-jobs is not supported.

        Args:
          job_id: The unique identifier of the job

          parent_id: The ID of the parent job, if any

          title: The title of the job

          use_parent_data: Indicates whether to use the parent job's data or not

          assign: Data related to job assignment

          code: The code of the job

          description: The description of the job

          gps: The GPS data of the job

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    def update(
        self,
        job_id: str,
        *,
        title: str,
        assign: AssignDataInParam | NotGiven = NOT_GIVEN,
        code: str | NotGiven = NOT_GIVEN,
        color: str | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        gps: GpsDataParam | NotGiven = NOT_GIVEN,
        instance_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIResponse:
        """Update a single job by its unique identifier.

        Currently, updating job with
        nested sub-jobs is not supported.

        Args:
          job_id: The unique identifier of the job

          title: The title of the job

          assign: Settings related to job assignment

          code: The code of the job

          color:
              The color associated with the job. Should be one of the following colors:
              ['#4B7AC5', '#801A1A', '#AE2121', '#DC7A7A', '#B0712E', '#D4985A', '#E4B37F',
              '#AE8E2D', '#CBA73A', '#D9B443', '#487037', '#6F9B5C', '#91B282', '#365C64',
              '#5687B3', '#7C9BA2', '#3968BB', '#85A6DA', '#225A8C', '#548CBE', '#81A8CC',
              '#4E3F75', '#604E8E', '#8679AA', '#983D73', '#A43778', '#D178AD', '#6B2E4C',
              '#925071', '#B57D9A', '#3a3a3a', '#616161', '#969696']

          description: The description of the job

          gps: The GPS data of the job

          instance_ids: List of instance ids (scheduler id or time clock id) to assign the job to

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["parent_id", "title", "use_parent_data"], ["title"])
    def update(
        self,
        job_id: str,
        *,
        parent_id: str | NotGiven = NOT_GIVEN,
        title: str,
        use_parent_data: bool | NotGiven = NOT_GIVEN,
        assign: AssignDataInParam | NotGiven = NOT_GIVEN,
        code: str | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        gps: GpsDataParam | NotGiven = NOT_GIVEN,
        color: str | NotGiven = NOT_GIVEN,
        instance_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIResponse:
        if not job_id:
            raise ValueError(f"Expected a non-empty value for `job_id` but received {job_id!r}")
        return self._put(
            f"/jobs/v1/jobs/{job_id}",
            body=maybe_transform(
                {
                    "parent_id": parent_id,
                    "title": title,
                    "use_parent_data": use_parent_data,
                    "assign": assign,
                    "code": code,
                    "description": description,
                    "gps": gps,
                    "color": color,
                    "instance_ids": instance_ids,
                },
                job_update_params.JobUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIResponse,
        )

    def list(
        self,
        *,
        include_deleted: bool | NotGiven = NOT_GIVEN,
        instance_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        job_codes: List[str] | NotGiven = NOT_GIVEN,
        job_ids: List[str] | NotGiven = NOT_GIVEN,
        job_names: List[str] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        order: SortOrder | NotGiven = NOT_GIVEN,
        sort: Literal["title"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> JobListResponse:
        """
        Get a list of job objects relevant to instance id (scheduler id or time clock
        id). If unified jobs are disabled, only schedulers are supported

        Args:
          include_deleted: Determines whether the response includes jobs that have been deleted. Default
              value is set to true.

          instance_ids: List of instance IDs (scheduler id or time clock id) to filter by

          job_codes: List of job codes to filter by. In case where a sub-job code is provided, the
              relevant sub-job with all other nested sub-jobs will be retrieved alongside with
              the parent job.

          job_ids: List of job IDs to filter by. In cases where a job ID includes nested sub-jobs,
              all sub-jobs under that parent job will be retrieved alongside with the parent
              job. Note that this filter does not support direct querying by sub-job IDs. To
              retrieve specific sub-jobs, please use the Get Job endpoint

          job_names: List of job names to filter by. In case where a sub-job name is provided, the
              relevant sub-job with all other nested sub-jobs will be retrieved alongside with
              the parent job.

          limit: The maximum number of results to display per page

          offset: The resource offset of the last successfully read resource will be returned as
              the paging.offset JSON property of a paginated response containing more results

          order: An enumeration.

          sort: An enumeration.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/jobs/v1/jobs",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "include_deleted": include_deleted,
                        "instance_ids": instance_ids,
                        "job_codes": job_codes,
                        "job_ids": job_ids,
                        "job_names": job_names,
                        "limit": limit,
                        "offset": offset,
                        "order": order,
                        "sort": sort,
                    },
                    job_list_params.JobListParams,
                ),
            ),
            cast_to=JobListResponse,
        )

    def delete(
        self,
        job_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> JobDeleteResponse:
        """Delete a single job by its unique identifier.

        Currently, deleting a sub-job
        and/or job with nested sub-jobs is not supported.

        Args:
          job_id: The unique identifier of the job

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not job_id:
            raise ValueError(f"Expected a non-empty value for `job_id` but received {job_id!r}")
        return self._delete(
            f"/jobs/v1/jobs/{job_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=JobDeleteResponse,
        )


class AsyncJobsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncJobsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncJobsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncJobsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/gil-zirlin/connecteam-sdk-python#with_streaming_response
        """
        return AsyncJobsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        body: Iterable[job_create_params.Body],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> JobCreateResponse:
        """
        Create individual or multiple jobs under a specified scheduler

        Args:
          body: Request model for the new Jobs

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/jobs/v1/jobs",
            body=await async_maybe_transform(body, Iterable[job_create_params.Body]),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=JobCreateResponse,
        )

    async def retrieve(
        self,
        job_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIResponse:
        """
        Retrieve a single job information by its unique ID

        Args:
          job_id: The unique identifier of the job

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not job_id:
            raise ValueError(f"Expected a non-empty value for `job_id` but received {job_id!r}")
        return await self._get(
            f"/jobs/v1/jobs/{job_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIResponse,
        )

    @overload
    async def update(
        self,
        job_id: str,
        *,
        parent_id: str,
        title: str,
        use_parent_data: bool,
        assign: AssignDataInParam | NotGiven = NOT_GIVEN,
        code: str | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        gps: GpsDataParam | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIResponse:
        """Update a single job by its unique identifier.

        Currently, updating job with
        nested sub-jobs is not supported.

        Args:
          job_id: The unique identifier of the job

          parent_id: The ID of the parent job, if any

          title: The title of the job

          use_parent_data: Indicates whether to use the parent job's data or not

          assign: Data related to job assignment

          code: The code of the job

          description: The description of the job

          gps: The GPS data of the job

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @overload
    async def update(
        self,
        job_id: str,
        *,
        title: str,
        assign: AssignDataInParam | NotGiven = NOT_GIVEN,
        code: str | NotGiven = NOT_GIVEN,
        color: str | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        gps: GpsDataParam | NotGiven = NOT_GIVEN,
        instance_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIResponse:
        """Update a single job by its unique identifier.

        Currently, updating job with
        nested sub-jobs is not supported.

        Args:
          job_id: The unique identifier of the job

          title: The title of the job

          assign: Settings related to job assignment

          code: The code of the job

          color:
              The color associated with the job. Should be one of the following colors:
              ['#4B7AC5', '#801A1A', '#AE2121', '#DC7A7A', '#B0712E', '#D4985A', '#E4B37F',
              '#AE8E2D', '#CBA73A', '#D9B443', '#487037', '#6F9B5C', '#91B282', '#365C64',
              '#5687B3', '#7C9BA2', '#3968BB', '#85A6DA', '#225A8C', '#548CBE', '#81A8CC',
              '#4E3F75', '#604E8E', '#8679AA', '#983D73', '#A43778', '#D178AD', '#6B2E4C',
              '#925071', '#B57D9A', '#3a3a3a', '#616161', '#969696']

          description: The description of the job

          gps: The GPS data of the job

          instance_ids: List of instance ids (scheduler id or time clock id) to assign the job to

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        ...

    @required_args(["parent_id", "title", "use_parent_data"], ["title"])
    async def update(
        self,
        job_id: str,
        *,
        parent_id: str | NotGiven = NOT_GIVEN,
        title: str,
        use_parent_data: bool | NotGiven = NOT_GIVEN,
        assign: AssignDataInParam | NotGiven = NOT_GIVEN,
        code: str | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        gps: GpsDataParam | NotGiven = NOT_GIVEN,
        color: str | NotGiven = NOT_GIVEN,
        instance_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> APIResponse:
        if not job_id:
            raise ValueError(f"Expected a non-empty value for `job_id` but received {job_id!r}")
        return await self._put(
            f"/jobs/v1/jobs/{job_id}",
            body=await async_maybe_transform(
                {
                    "parent_id": parent_id,
                    "title": title,
                    "use_parent_data": use_parent_data,
                    "assign": assign,
                    "code": code,
                    "description": description,
                    "gps": gps,
                    "color": color,
                    "instance_ids": instance_ids,
                },
                job_update_params.JobUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=APIResponse,
        )

    async def list(
        self,
        *,
        include_deleted: bool | NotGiven = NOT_GIVEN,
        instance_ids: Iterable[int] | NotGiven = NOT_GIVEN,
        job_codes: List[str] | NotGiven = NOT_GIVEN,
        job_ids: List[str] | NotGiven = NOT_GIVEN,
        job_names: List[str] | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        offset: int | NotGiven = NOT_GIVEN,
        order: SortOrder | NotGiven = NOT_GIVEN,
        sort: Literal["title"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> JobListResponse:
        """
        Get a list of job objects relevant to instance id (scheduler id or time clock
        id). If unified jobs are disabled, only schedulers are supported

        Args:
          include_deleted: Determines whether the response includes jobs that have been deleted. Default
              value is set to true.

          instance_ids: List of instance IDs (scheduler id or time clock id) to filter by

          job_codes: List of job codes to filter by. In case where a sub-job code is provided, the
              relevant sub-job with all other nested sub-jobs will be retrieved alongside with
              the parent job.

          job_ids: List of job IDs to filter by. In cases where a job ID includes nested sub-jobs,
              all sub-jobs under that parent job will be retrieved alongside with the parent
              job. Note that this filter does not support direct querying by sub-job IDs. To
              retrieve specific sub-jobs, please use the Get Job endpoint

          job_names: List of job names to filter by. In case where a sub-job name is provided, the
              relevant sub-job with all other nested sub-jobs will be retrieved alongside with
              the parent job.

          limit: The maximum number of results to display per page

          offset: The resource offset of the last successfully read resource will be returned as
              the paging.offset JSON property of a paginated response containing more results

          order: An enumeration.

          sort: An enumeration.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/jobs/v1/jobs",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "include_deleted": include_deleted,
                        "instance_ids": instance_ids,
                        "job_codes": job_codes,
                        "job_ids": job_ids,
                        "job_names": job_names,
                        "limit": limit,
                        "offset": offset,
                        "order": order,
                        "sort": sort,
                    },
                    job_list_params.JobListParams,
                ),
            ),
            cast_to=JobListResponse,
        )

    async def delete(
        self,
        job_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> JobDeleteResponse:
        """Delete a single job by its unique identifier.

        Currently, deleting a sub-job
        and/or job with nested sub-jobs is not supported.

        Args:
          job_id: The unique identifier of the job

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not job_id:
            raise ValueError(f"Expected a non-empty value for `job_id` but received {job_id!r}")
        return await self._delete(
            f"/jobs/v1/jobs/{job_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=JobDeleteResponse,
        )


class JobsResourceWithRawResponse:
    def __init__(self, jobs: JobsResource) -> None:
        self._jobs = jobs

        self.create = to_raw_response_wrapper(
            jobs.create,
        )
        self.retrieve = to_raw_response_wrapper(
            jobs.retrieve,
        )
        self.update = to_raw_response_wrapper(
            jobs.update,
        )
        self.list = to_raw_response_wrapper(
            jobs.list,
        )
        self.delete = to_raw_response_wrapper(
            jobs.delete,
        )


class AsyncJobsResourceWithRawResponse:
    def __init__(self, jobs: AsyncJobsResource) -> None:
        self._jobs = jobs

        self.create = async_to_raw_response_wrapper(
            jobs.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            jobs.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            jobs.update,
        )
        self.list = async_to_raw_response_wrapper(
            jobs.list,
        )
        self.delete = async_to_raw_response_wrapper(
            jobs.delete,
        )


class JobsResourceWithStreamingResponse:
    def __init__(self, jobs: JobsResource) -> None:
        self._jobs = jobs

        self.create = to_streamed_response_wrapper(
            jobs.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            jobs.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            jobs.update,
        )
        self.list = to_streamed_response_wrapper(
            jobs.list,
        )
        self.delete = to_streamed_response_wrapper(
            jobs.delete,
        )


class AsyncJobsResourceWithStreamingResponse:
    def __init__(self, jobs: AsyncJobsResource) -> None:
        self._jobs = jobs

        self.create = async_to_streamed_response_wrapper(
            jobs.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            jobs.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            jobs.update,
        )
        self.list = async_to_streamed_response_wrapper(
            jobs.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            jobs.delete,
        )
