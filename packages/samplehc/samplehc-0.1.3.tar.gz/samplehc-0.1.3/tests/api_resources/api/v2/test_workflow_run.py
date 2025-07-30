# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from samplehc import SampleHealthcare, AsyncSampleHealthcare
from tests.utils import assert_matches_type
from samplehc.types.api.v2 import (
    WorkflowRunRetrieveStartDataResponse,
    WorkflowRunResumeWhenCompleteResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestWorkflowRun:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_cancel(self, client: SampleHealthcare) -> None:
        workflow_run = client.api.v2.workflow_run.cancel(
            "workflowRunId",
        )
        assert_matches_type(object, workflow_run, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_cancel(self, client: SampleHealthcare) -> None:
        response = client.api.v2.workflow_run.with_raw_response.cancel(
            "workflowRunId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workflow_run = response.parse()
        assert_matches_type(object, workflow_run, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_cancel(self, client: SampleHealthcare) -> None:
        with client.api.v2.workflow_run.with_streaming_response.cancel(
            "workflowRunId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workflow_run = response.parse()
            assert_matches_type(object, workflow_run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_cancel(self, client: SampleHealthcare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workflow_run_id` but received ''"):
            client.api.v2.workflow_run.with_raw_response.cancel(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_resume_when_complete(self, client: SampleHealthcare) -> None:
        workflow_run = client.api.v2.workflow_run.resume_when_complete(
            async_result_id="asyncResultId",
        )
        assert_matches_type(WorkflowRunResumeWhenCompleteResponse, workflow_run, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_resume_when_complete(self, client: SampleHealthcare) -> None:
        response = client.api.v2.workflow_run.with_raw_response.resume_when_complete(
            async_result_id="asyncResultId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workflow_run = response.parse()
        assert_matches_type(WorkflowRunResumeWhenCompleteResponse, workflow_run, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_resume_when_complete(self, client: SampleHealthcare) -> None:
        with client.api.v2.workflow_run.with_streaming_response.resume_when_complete(
            async_result_id="asyncResultId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workflow_run = response.parse()
            assert_matches_type(WorkflowRunResumeWhenCompleteResponse, workflow_run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_start_data(self, client: SampleHealthcare) -> None:
        workflow_run = client.api.v2.workflow_run.retrieve_start_data()
        assert_matches_type(WorkflowRunRetrieveStartDataResponse, workflow_run, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve_start_data(self, client: SampleHealthcare) -> None:
        response = client.api.v2.workflow_run.with_raw_response.retrieve_start_data()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workflow_run = response.parse()
        assert_matches_type(WorkflowRunRetrieveStartDataResponse, workflow_run, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve_start_data(self, client: SampleHealthcare) -> None:
        with client.api.v2.workflow_run.with_streaming_response.retrieve_start_data() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workflow_run = response.parse()
            assert_matches_type(WorkflowRunRetrieveStartDataResponse, workflow_run, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncWorkflowRun:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_cancel(self, async_client: AsyncSampleHealthcare) -> None:
        workflow_run = await async_client.api.v2.workflow_run.cancel(
            "workflowRunId",
        )
        assert_matches_type(object, workflow_run, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_cancel(self, async_client: AsyncSampleHealthcare) -> None:
        response = await async_client.api.v2.workflow_run.with_raw_response.cancel(
            "workflowRunId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workflow_run = await response.parse()
        assert_matches_type(object, workflow_run, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_cancel(self, async_client: AsyncSampleHealthcare) -> None:
        async with async_client.api.v2.workflow_run.with_streaming_response.cancel(
            "workflowRunId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workflow_run = await response.parse()
            assert_matches_type(object, workflow_run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_cancel(self, async_client: AsyncSampleHealthcare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workflow_run_id` but received ''"):
            await async_client.api.v2.workflow_run.with_raw_response.cancel(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_resume_when_complete(self, async_client: AsyncSampleHealthcare) -> None:
        workflow_run = await async_client.api.v2.workflow_run.resume_when_complete(
            async_result_id="asyncResultId",
        )
        assert_matches_type(WorkflowRunResumeWhenCompleteResponse, workflow_run, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_resume_when_complete(self, async_client: AsyncSampleHealthcare) -> None:
        response = await async_client.api.v2.workflow_run.with_raw_response.resume_when_complete(
            async_result_id="asyncResultId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workflow_run = await response.parse()
        assert_matches_type(WorkflowRunResumeWhenCompleteResponse, workflow_run, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_resume_when_complete(self, async_client: AsyncSampleHealthcare) -> None:
        async with async_client.api.v2.workflow_run.with_streaming_response.resume_when_complete(
            async_result_id="asyncResultId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workflow_run = await response.parse()
            assert_matches_type(WorkflowRunResumeWhenCompleteResponse, workflow_run, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_start_data(self, async_client: AsyncSampleHealthcare) -> None:
        workflow_run = await async_client.api.v2.workflow_run.retrieve_start_data()
        assert_matches_type(WorkflowRunRetrieveStartDataResponse, workflow_run, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve_start_data(self, async_client: AsyncSampleHealthcare) -> None:
        response = await async_client.api.v2.workflow_run.with_raw_response.retrieve_start_data()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workflow_run = await response.parse()
        assert_matches_type(WorkflowRunRetrieveStartDataResponse, workflow_run, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve_start_data(self, async_client: AsyncSampleHealthcare) -> None:
        async with async_client.api.v2.workflow_run.with_streaming_response.retrieve_start_data() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workflow_run = await response.parse()
            assert_matches_type(WorkflowRunRetrieveStartDataResponse, workflow_run, path=["response"])

        assert cast(Any, response.is_closed) is True
