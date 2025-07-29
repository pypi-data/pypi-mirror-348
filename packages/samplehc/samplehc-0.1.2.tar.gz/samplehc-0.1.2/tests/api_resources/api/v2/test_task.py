# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from samplehc import SampleHealthcare, AsyncSampleHealthcare
from tests.utils import assert_matches_type
from samplehc.types.api.v2 import TaskCompleteResponse, TaskGetSuspendedPayloadResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTask:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_complete(self, client: SampleHealthcare) -> None:
        task = client.api.v2.task.complete(
            task_id="taskId",
        )
        assert_matches_type(TaskCompleteResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_complete_with_all_params(self, client: SampleHealthcare) -> None:
        task = client.api.v2.task.complete(
            task_id="taskId",
            result={},
        )
        assert_matches_type(TaskCompleteResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_complete(self, client: SampleHealthcare) -> None:
        response = client.api.v2.task.with_raw_response.complete(
            task_id="taskId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = response.parse()
        assert_matches_type(TaskCompleteResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_complete(self, client: SampleHealthcare) -> None:
        with client.api.v2.task.with_streaming_response.complete(
            task_id="taskId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = response.parse()
            assert_matches_type(TaskCompleteResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_complete(self, client: SampleHealthcare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            client.api.v2.task.with_raw_response.complete(
                task_id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_get_suspended_payload(self, client: SampleHealthcare) -> None:
        task = client.api.v2.task.get_suspended_payload(
            "taskId",
        )
        assert_matches_type(TaskGetSuspendedPayloadResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_suspended_payload(self, client: SampleHealthcare) -> None:
        response = client.api.v2.task.with_raw_response.get_suspended_payload(
            "taskId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = response.parse()
        assert_matches_type(TaskGetSuspendedPayloadResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_suspended_payload(self, client: SampleHealthcare) -> None:
        with client.api.v2.task.with_streaming_response.get_suspended_payload(
            "taskId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = response.parse()
            assert_matches_type(TaskGetSuspendedPayloadResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_get_suspended_payload(self, client: SampleHealthcare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            client.api.v2.task.with_raw_response.get_suspended_payload(
                "",
            )


class TestAsyncTask:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_complete(self, async_client: AsyncSampleHealthcare) -> None:
        task = await async_client.api.v2.task.complete(
            task_id="taskId",
        )
        assert_matches_type(TaskCompleteResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_complete_with_all_params(self, async_client: AsyncSampleHealthcare) -> None:
        task = await async_client.api.v2.task.complete(
            task_id="taskId",
            result={},
        )
        assert_matches_type(TaskCompleteResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_complete(self, async_client: AsyncSampleHealthcare) -> None:
        response = await async_client.api.v2.task.with_raw_response.complete(
            task_id="taskId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = await response.parse()
        assert_matches_type(TaskCompleteResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_complete(self, async_client: AsyncSampleHealthcare) -> None:
        async with async_client.api.v2.task.with_streaming_response.complete(
            task_id="taskId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = await response.parse()
            assert_matches_type(TaskCompleteResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_complete(self, async_client: AsyncSampleHealthcare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            await async_client.api.v2.task.with_raw_response.complete(
                task_id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_suspended_payload(self, async_client: AsyncSampleHealthcare) -> None:
        task = await async_client.api.v2.task.get_suspended_payload(
            "taskId",
        )
        assert_matches_type(TaskGetSuspendedPayloadResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_suspended_payload(self, async_client: AsyncSampleHealthcare) -> None:
        response = await async_client.api.v2.task.with_raw_response.get_suspended_payload(
            "taskId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        task = await response.parse()
        assert_matches_type(TaskGetSuspendedPayloadResponse, task, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_suspended_payload(self, async_client: AsyncSampleHealthcare) -> None:
        async with async_client.api.v2.task.with_streaming_response.get_suspended_payload(
            "taskId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            task = await response.parse()
            assert_matches_type(TaskGetSuspendedPayloadResponse, task, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_get_suspended_payload(self, async_client: AsyncSampleHealthcare) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `task_id` but received ''"):
            await async_client.api.v2.task.with_raw_response.get_suspended_payload(
                "",
            )
