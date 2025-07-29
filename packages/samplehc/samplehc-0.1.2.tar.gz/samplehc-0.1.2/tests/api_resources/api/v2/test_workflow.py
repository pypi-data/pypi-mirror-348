# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from samplehc import SampleHealthcare, AsyncSampleHealthcare
from tests.utils import assert_matches_type
from samplehc.types.api.v2 import WorkflowStartResponse, WorkflowDeployResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestWorkflow:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_deploy(self, client: SampleHealthcare) -> None:
        workflow = client.api.v2.workflow.deploy(
            "workflowId",
        )
        assert_matches_type(WorkflowDeployResponse, workflow, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_deploy(self, client: SampleHealthcare) -> None:
        response = client.api.v2.workflow.with_raw_response.deploy(
            "workflowId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workflow = response.parse()
        assert_matches_type(WorkflowDeployResponse, workflow, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_deploy(self, client: SampleHealthcare) -> None:
        with client.api.v2.workflow.with_streaming_response.deploy(
            "workflowId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workflow = response.parse()
            assert_matches_type(WorkflowDeployResponse, workflow, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_deploy(self, client: SampleHealthcare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workflow_id` but received ''"):
            client.api.v2.workflow.with_raw_response.deploy(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_start(self, client: SampleHealthcare) -> None:
        workflow = client.api.v2.workflow.start(
            workflow_slug="workflowSlug",
        )
        assert_matches_type(WorkflowStartResponse, workflow, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_start_with_all_params(self, client: SampleHealthcare) -> None:
        workflow = client.api.v2.workflow.start(
            workflow_slug="workflowSlug",
            body={},
        )
        assert_matches_type(WorkflowStartResponse, workflow, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_start(self, client: SampleHealthcare) -> None:
        response = client.api.v2.workflow.with_raw_response.start(
            workflow_slug="workflowSlug",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workflow = response.parse()
        assert_matches_type(WorkflowStartResponse, workflow, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_start(self, client: SampleHealthcare) -> None:
        with client.api.v2.workflow.with_streaming_response.start(
            workflow_slug="workflowSlug",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workflow = response.parse()
            assert_matches_type(WorkflowStartResponse, workflow, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_start(self, client: SampleHealthcare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workflow_slug` but received ''"):
            client.api.v2.workflow.with_raw_response.start(
                workflow_slug="",
            )


class TestAsyncWorkflow:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_deploy(self, async_client: AsyncSampleHealthcare) -> None:
        workflow = await async_client.api.v2.workflow.deploy(
            "workflowId",
        )
        assert_matches_type(WorkflowDeployResponse, workflow, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_deploy(self, async_client: AsyncSampleHealthcare) -> None:
        response = await async_client.api.v2.workflow.with_raw_response.deploy(
            "workflowId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workflow = await response.parse()
        assert_matches_type(WorkflowDeployResponse, workflow, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_deploy(self, async_client: AsyncSampleHealthcare) -> None:
        async with async_client.api.v2.workflow.with_streaming_response.deploy(
            "workflowId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workflow = await response.parse()
            assert_matches_type(WorkflowDeployResponse, workflow, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_deploy(self, async_client: AsyncSampleHealthcare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workflow_id` but received ''"):
            await async_client.api.v2.workflow.with_raw_response.deploy(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_start(self, async_client: AsyncSampleHealthcare) -> None:
        workflow = await async_client.api.v2.workflow.start(
            workflow_slug="workflowSlug",
        )
        assert_matches_type(WorkflowStartResponse, workflow, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_start_with_all_params(self, async_client: AsyncSampleHealthcare) -> None:
        workflow = await async_client.api.v2.workflow.start(
            workflow_slug="workflowSlug",
            body={},
        )
        assert_matches_type(WorkflowStartResponse, workflow, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_start(self, async_client: AsyncSampleHealthcare) -> None:
        response = await async_client.api.v2.workflow.with_raw_response.start(
            workflow_slug="workflowSlug",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        workflow = await response.parse()
        assert_matches_type(WorkflowStartResponse, workflow, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_start(self, async_client: AsyncSampleHealthcare) -> None:
        async with async_client.api.v2.workflow.with_streaming_response.start(
            workflow_slug="workflowSlug",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            workflow = await response.parse()
            assert_matches_type(WorkflowStartResponse, workflow, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_start(self, async_client: AsyncSampleHealthcare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `workflow_slug` but received ''"):
            await async_client.api.v2.workflow.with_raw_response.start(
                workflow_slug="",
            )
