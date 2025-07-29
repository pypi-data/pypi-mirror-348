# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .task import (
    TaskResource,
    AsyncTaskResource,
    TaskResourceWithRawResponse,
    AsyncTaskResourceWithRawResponse,
    TaskResourceWithStreamingResponse,
    AsyncTaskResourceWithStreamingResponse,
)
from .ledger import (
    LedgerResource,
    AsyncLedgerResource,
    LedgerResourceWithRawResponse,
    AsyncLedgerResourceWithRawResponse,
    LedgerResourceWithStreamingResponse,
    AsyncLedgerResourceWithStreamingResponse,
)
from .workflow import (
    WorkflowResource,
    AsyncWorkflowResource,
    WorkflowResourceWithRawResponse,
    AsyncWorkflowResourceWithRawResponse,
    WorkflowResourceWithStreamingResponse,
    AsyncWorkflowResourceWithStreamingResponse,
)
from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .communication import (
    CommunicationResource,
    AsyncCommunicationResource,
    CommunicationResourceWithRawResponse,
    AsyncCommunicationResourceWithRawResponse,
    CommunicationResourceWithStreamingResponse,
    AsyncCommunicationResourceWithStreamingResponse,
)
from ...._base_client import make_request_options
from .document.document import (
    DocumentResource,
    AsyncDocumentResource,
    DocumentResourceWithRawResponse,
    AsyncDocumentResourceWithRawResponse,
    DocumentResourceWithStreamingResponse,
    AsyncDocumentResourceWithStreamingResponse,
)
from .workflow_run.workflow_run import (
    WorkflowRunResource,
    AsyncWorkflowRunResource,
    WorkflowRunResourceWithRawResponse,
    AsyncWorkflowRunResourceWithRawResponse,
    WorkflowRunResourceWithStreamingResponse,
    AsyncWorkflowRunResourceWithStreamingResponse,
)
from .clearinghouse.clearinghouse import (
    ClearinghouseResource,
    AsyncClearinghouseResource,
    ClearinghouseResourceWithRawResponse,
    AsyncClearinghouseResourceWithRawResponse,
    ClearinghouseResourceWithStreamingResponse,
    AsyncClearinghouseResourceWithStreamingResponse,
)
from ....types.api.v2_get_async_result_response import V2GetAsyncResultResponse

__all__ = ["V2Resource", "AsyncV2Resource"]


class V2Resource(SyncAPIResource):
    @cached_property
    def workflow_run(self) -> WorkflowRunResource:
        return WorkflowRunResource(self._client)

    @cached_property
    def task(self) -> TaskResource:
        return TaskResource(self._client)

    @cached_property
    def workflow(self) -> WorkflowResource:
        return WorkflowResource(self._client)

    @cached_property
    def document(self) -> DocumentResource:
        return DocumentResource(self._client)

    @cached_property
    def communication(self) -> CommunicationResource:
        return CommunicationResource(self._client)

    @cached_property
    def ledger(self) -> LedgerResource:
        return LedgerResource(self._client)

    @cached_property
    def clearinghouse(self) -> ClearinghouseResource:
        return ClearinghouseResource(self._client)

    @cached_property
    def with_raw_response(self) -> V2ResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/samplehc/samplehc-python#accessing-raw-response-data-eg-headers
        """
        return V2ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> V2ResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/samplehc/samplehc-python#with_streaming_response
        """
        return V2ResourceWithStreamingResponse(self)

    def get_async_result(
        self,
        async_result_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> V2GetAsyncResultResponse:
        """
        Retrieves the status and result of an asynchronous operation.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not async_result_id:
            raise ValueError(f"Expected a non-empty value for `async_result_id` but received {async_result_id!r}")
        return self._get(
            f"/api/v2/async-result/{async_result_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V2GetAsyncResultResponse,
        )


class AsyncV2Resource(AsyncAPIResource):
    @cached_property
    def workflow_run(self) -> AsyncWorkflowRunResource:
        return AsyncWorkflowRunResource(self._client)

    @cached_property
    def task(self) -> AsyncTaskResource:
        return AsyncTaskResource(self._client)

    @cached_property
    def workflow(self) -> AsyncWorkflowResource:
        return AsyncWorkflowResource(self._client)

    @cached_property
    def document(self) -> AsyncDocumentResource:
        return AsyncDocumentResource(self._client)

    @cached_property
    def communication(self) -> AsyncCommunicationResource:
        return AsyncCommunicationResource(self._client)

    @cached_property
    def ledger(self) -> AsyncLedgerResource:
        return AsyncLedgerResource(self._client)

    @cached_property
    def clearinghouse(self) -> AsyncClearinghouseResource:
        return AsyncClearinghouseResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncV2ResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/samplehc/samplehc-python#accessing-raw-response-data-eg-headers
        """
        return AsyncV2ResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncV2ResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/samplehc/samplehc-python#with_streaming_response
        """
        return AsyncV2ResourceWithStreamingResponse(self)

    async def get_async_result(
        self,
        async_result_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> V2GetAsyncResultResponse:
        """
        Retrieves the status and result of an asynchronous operation.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not async_result_id:
            raise ValueError(f"Expected a non-empty value for `async_result_id` but received {async_result_id!r}")
        return await self._get(
            f"/api/v2/async-result/{async_result_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=V2GetAsyncResultResponse,
        )


class V2ResourceWithRawResponse:
    def __init__(self, v2: V2Resource) -> None:
        self._v2 = v2

        self.get_async_result = to_raw_response_wrapper(
            v2.get_async_result,
        )

    @cached_property
    def workflow_run(self) -> WorkflowRunResourceWithRawResponse:
        return WorkflowRunResourceWithRawResponse(self._v2.workflow_run)

    @cached_property
    def task(self) -> TaskResourceWithRawResponse:
        return TaskResourceWithRawResponse(self._v2.task)

    @cached_property
    def workflow(self) -> WorkflowResourceWithRawResponse:
        return WorkflowResourceWithRawResponse(self._v2.workflow)

    @cached_property
    def document(self) -> DocumentResourceWithRawResponse:
        return DocumentResourceWithRawResponse(self._v2.document)

    @cached_property
    def communication(self) -> CommunicationResourceWithRawResponse:
        return CommunicationResourceWithRawResponse(self._v2.communication)

    @cached_property
    def ledger(self) -> LedgerResourceWithRawResponse:
        return LedgerResourceWithRawResponse(self._v2.ledger)

    @cached_property
    def clearinghouse(self) -> ClearinghouseResourceWithRawResponse:
        return ClearinghouseResourceWithRawResponse(self._v2.clearinghouse)


class AsyncV2ResourceWithRawResponse:
    def __init__(self, v2: AsyncV2Resource) -> None:
        self._v2 = v2

        self.get_async_result = async_to_raw_response_wrapper(
            v2.get_async_result,
        )

    @cached_property
    def workflow_run(self) -> AsyncWorkflowRunResourceWithRawResponse:
        return AsyncWorkflowRunResourceWithRawResponse(self._v2.workflow_run)

    @cached_property
    def task(self) -> AsyncTaskResourceWithRawResponse:
        return AsyncTaskResourceWithRawResponse(self._v2.task)

    @cached_property
    def workflow(self) -> AsyncWorkflowResourceWithRawResponse:
        return AsyncWorkflowResourceWithRawResponse(self._v2.workflow)

    @cached_property
    def document(self) -> AsyncDocumentResourceWithRawResponse:
        return AsyncDocumentResourceWithRawResponse(self._v2.document)

    @cached_property
    def communication(self) -> AsyncCommunicationResourceWithRawResponse:
        return AsyncCommunicationResourceWithRawResponse(self._v2.communication)

    @cached_property
    def ledger(self) -> AsyncLedgerResourceWithRawResponse:
        return AsyncLedgerResourceWithRawResponse(self._v2.ledger)

    @cached_property
    def clearinghouse(self) -> AsyncClearinghouseResourceWithRawResponse:
        return AsyncClearinghouseResourceWithRawResponse(self._v2.clearinghouse)


class V2ResourceWithStreamingResponse:
    def __init__(self, v2: V2Resource) -> None:
        self._v2 = v2

        self.get_async_result = to_streamed_response_wrapper(
            v2.get_async_result,
        )

    @cached_property
    def workflow_run(self) -> WorkflowRunResourceWithStreamingResponse:
        return WorkflowRunResourceWithStreamingResponse(self._v2.workflow_run)

    @cached_property
    def task(self) -> TaskResourceWithStreamingResponse:
        return TaskResourceWithStreamingResponse(self._v2.task)

    @cached_property
    def workflow(self) -> WorkflowResourceWithStreamingResponse:
        return WorkflowResourceWithStreamingResponse(self._v2.workflow)

    @cached_property
    def document(self) -> DocumentResourceWithStreamingResponse:
        return DocumentResourceWithStreamingResponse(self._v2.document)

    @cached_property
    def communication(self) -> CommunicationResourceWithStreamingResponse:
        return CommunicationResourceWithStreamingResponse(self._v2.communication)

    @cached_property
    def ledger(self) -> LedgerResourceWithStreamingResponse:
        return LedgerResourceWithStreamingResponse(self._v2.ledger)

    @cached_property
    def clearinghouse(self) -> ClearinghouseResourceWithStreamingResponse:
        return ClearinghouseResourceWithStreamingResponse(self._v2.clearinghouse)


class AsyncV2ResourceWithStreamingResponse:
    def __init__(self, v2: AsyncV2Resource) -> None:
        self._v2 = v2

        self.get_async_result = async_to_streamed_response_wrapper(
            v2.get_async_result,
        )

    @cached_property
    def workflow_run(self) -> AsyncWorkflowRunResourceWithStreamingResponse:
        return AsyncWorkflowRunResourceWithStreamingResponse(self._v2.workflow_run)

    @cached_property
    def task(self) -> AsyncTaskResourceWithStreamingResponse:
        return AsyncTaskResourceWithStreamingResponse(self._v2.task)

    @cached_property
    def workflow(self) -> AsyncWorkflowResourceWithStreamingResponse:
        return AsyncWorkflowResourceWithStreamingResponse(self._v2.workflow)

    @cached_property
    def document(self) -> AsyncDocumentResourceWithStreamingResponse:
        return AsyncDocumentResourceWithStreamingResponse(self._v2.document)

    @cached_property
    def communication(self) -> AsyncCommunicationResourceWithStreamingResponse:
        return AsyncCommunicationResourceWithStreamingResponse(self._v2.communication)

    @cached_property
    def ledger(self) -> AsyncLedgerResourceWithStreamingResponse:
        return AsyncLedgerResourceWithStreamingResponse(self._v2.ledger)

    @cached_property
    def clearinghouse(self) -> AsyncClearinghouseResourceWithStreamingResponse:
        return AsyncClearinghouseResourceWithStreamingResponse(self._v2.clearinghouse)
