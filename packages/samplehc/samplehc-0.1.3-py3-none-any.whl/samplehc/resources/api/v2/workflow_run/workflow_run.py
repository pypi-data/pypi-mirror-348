# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .step import (
    StepResource,
    AsyncStepResource,
    StepResourceWithRawResponse,
    AsyncStepResourceWithRawResponse,
    StepResourceWithStreamingResponse,
    AsyncStepResourceWithStreamingResponse,
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
from .....types.api.v2 import workflow_run_resume_when_complete_params
from .....types.api.v2.workflow_run_retrieve_start_data_response import WorkflowRunRetrieveStartDataResponse
from .....types.api.v2.workflow_run_resume_when_complete_response import WorkflowRunResumeWhenCompleteResponse

__all__ = ["WorkflowRunResource", "AsyncWorkflowRunResource"]


class WorkflowRunResource(SyncAPIResource):
    @cached_property
    def step(self) -> StepResource:
        return StepResource(self._client)

    @cached_property
    def with_raw_response(self) -> WorkflowRunResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/samplehc/samplehc-python#accessing-raw-response-data-eg-headers
        """
        return WorkflowRunResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> WorkflowRunResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/samplehc/samplehc-python#with_streaming_response
        """
        return WorkflowRunResourceWithStreamingResponse(self)

    def cancel(
        self,
        workflow_run_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """Requests cancellation of a currently active workflow run.

        This is an
        asynchronous operation and the run may take some time to fully stop.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workflow_run_id:
            raise ValueError(f"Expected a non-empty value for `workflow_run_id` but received {workflow_run_id!r}")
        return self._put(
            f"/api/v2/workflow-run/{workflow_run_id}/cancel",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    def resume_when_complete(
        self,
        *,
        async_result_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WorkflowRunResumeWhenCompleteResponse:
        """
        Registers an asynchronous task's result ID to resume a workflow run upon its
        completion. This endpoint requires an ExecuteStepRequestContext with
        `workflowRunId` and `stepAddr`.

        Args:
          async_result_id: The unique identifier of the asynchronous result to monitor before resuming.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/workflow-run/resume-when-complete",
            body=maybe_transform(
                {"async_result_id": async_result_id},
                workflow_run_resume_when_complete_params.WorkflowRunResumeWhenCompleteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkflowRunResumeWhenCompleteResponse,
        )

    def retrieve_start_data(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WorkflowRunRetrieveStartDataResponse:
        """
        Retrieves the initial data (startData) that was used to initiate the current
        workflow run. This endpoint requires an ExecuteStepRequestContext with a
        `workflowRunId`.
        """
        return self._get(
            "/api/v2/workflow-run/start-data",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkflowRunRetrieveStartDataResponse,
        )


class AsyncWorkflowRunResource(AsyncAPIResource):
    @cached_property
    def step(self) -> AsyncStepResource:
        return AsyncStepResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncWorkflowRunResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/samplehc/samplehc-python#accessing-raw-response-data-eg-headers
        """
        return AsyncWorkflowRunResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncWorkflowRunResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/samplehc/samplehc-python#with_streaming_response
        """
        return AsyncWorkflowRunResourceWithStreamingResponse(self)

    async def cancel(
        self,
        workflow_run_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """Requests cancellation of a currently active workflow run.

        This is an
        asynchronous operation and the run may take some time to fully stop.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not workflow_run_id:
            raise ValueError(f"Expected a non-empty value for `workflow_run_id` but received {workflow_run_id!r}")
        return await self._put(
            f"/api/v2/workflow-run/{workflow_run_id}/cancel",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )

    async def resume_when_complete(
        self,
        *,
        async_result_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WorkflowRunResumeWhenCompleteResponse:
        """
        Registers an asynchronous task's result ID to resume a workflow run upon its
        completion. This endpoint requires an ExecuteStepRequestContext with
        `workflowRunId` and `stepAddr`.

        Args:
          async_result_id: The unique identifier of the asynchronous result to monitor before resuming.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/workflow-run/resume-when-complete",
            body=await async_maybe_transform(
                {"async_result_id": async_result_id},
                workflow_run_resume_when_complete_params.WorkflowRunResumeWhenCompleteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkflowRunResumeWhenCompleteResponse,
        )

    async def retrieve_start_data(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WorkflowRunRetrieveStartDataResponse:
        """
        Retrieves the initial data (startData) that was used to initiate the current
        workflow run. This endpoint requires an ExecuteStepRequestContext with a
        `workflowRunId`.
        """
        return await self._get(
            "/api/v2/workflow-run/start-data",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WorkflowRunRetrieveStartDataResponse,
        )


class WorkflowRunResourceWithRawResponse:
    def __init__(self, workflow_run: WorkflowRunResource) -> None:
        self._workflow_run = workflow_run

        self.cancel = to_raw_response_wrapper(
            workflow_run.cancel,
        )
        self.resume_when_complete = to_raw_response_wrapper(
            workflow_run.resume_when_complete,
        )
        self.retrieve_start_data = to_raw_response_wrapper(
            workflow_run.retrieve_start_data,
        )

    @cached_property
    def step(self) -> StepResourceWithRawResponse:
        return StepResourceWithRawResponse(self._workflow_run.step)


class AsyncWorkflowRunResourceWithRawResponse:
    def __init__(self, workflow_run: AsyncWorkflowRunResource) -> None:
        self._workflow_run = workflow_run

        self.cancel = async_to_raw_response_wrapper(
            workflow_run.cancel,
        )
        self.resume_when_complete = async_to_raw_response_wrapper(
            workflow_run.resume_when_complete,
        )
        self.retrieve_start_data = async_to_raw_response_wrapper(
            workflow_run.retrieve_start_data,
        )

    @cached_property
    def step(self) -> AsyncStepResourceWithRawResponse:
        return AsyncStepResourceWithRawResponse(self._workflow_run.step)


class WorkflowRunResourceWithStreamingResponse:
    def __init__(self, workflow_run: WorkflowRunResource) -> None:
        self._workflow_run = workflow_run

        self.cancel = to_streamed_response_wrapper(
            workflow_run.cancel,
        )
        self.resume_when_complete = to_streamed_response_wrapper(
            workflow_run.resume_when_complete,
        )
        self.retrieve_start_data = to_streamed_response_wrapper(
            workflow_run.retrieve_start_data,
        )

    @cached_property
    def step(self) -> StepResourceWithStreamingResponse:
        return StepResourceWithStreamingResponse(self._workflow_run.step)


class AsyncWorkflowRunResourceWithStreamingResponse:
    def __init__(self, workflow_run: AsyncWorkflowRunResource) -> None:
        self._workflow_run = workflow_run

        self.cancel = async_to_streamed_response_wrapper(
            workflow_run.cancel,
        )
        self.resume_when_complete = async_to_streamed_response_wrapper(
            workflow_run.resume_when_complete,
        )
        self.retrieve_start_data = async_to_streamed_response_wrapper(
            workflow_run.retrieve_start_data,
        )

    @cached_property
    def step(self) -> AsyncStepResourceWithStreamingResponse:
        return AsyncStepResourceWithStreamingResponse(self._workflow_run.step)
