# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from samplehc import SampleHealthcare, AsyncSampleHealthcare
from tests.utils import assert_matches_type
from samplehc.types.api.v2.workflow_run import StepOutputResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestStep:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_output(self, client: SampleHealthcare) -> None:
        step = client.api.v2.workflow_run.step.output(
            "stepId",
        )
        assert_matches_type(StepOutputResponse, step, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_output(self, client: SampleHealthcare) -> None:
        response = client.api.v2.workflow_run.step.with_raw_response.output(
            "stepId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        step = response.parse()
        assert_matches_type(StepOutputResponse, step, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_output(self, client: SampleHealthcare) -> None:
        with client.api.v2.workflow_run.step.with_streaming_response.output(
            "stepId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            step = response.parse()
            assert_matches_type(StepOutputResponse, step, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_output(self, client: SampleHealthcare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `step_id` but received ''"):
            client.api.v2.workflow_run.step.with_raw_response.output(
                "",
            )


class TestAsyncStep:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_output(self, async_client: AsyncSampleHealthcare) -> None:
        step = await async_client.api.v2.workflow_run.step.output(
            "stepId",
        )
        assert_matches_type(StepOutputResponse, step, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_output(self, async_client: AsyncSampleHealthcare) -> None:
        response = await async_client.api.v2.workflow_run.step.with_raw_response.output(
            "stepId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        step = await response.parse()
        assert_matches_type(StepOutputResponse, step, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_output(self, async_client: AsyncSampleHealthcare) -> None:
        async with async_client.api.v2.workflow_run.step.with_streaming_response.output(
            "stepId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            step = await response.parse()
            assert_matches_type(StepOutputResponse, step, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_output(self, async_client: AsyncSampleHealthcare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `step_id` but received ''"):
            await async_client.api.v2.workflow_run.step.with_raw_response.output(
                "",
            )
