# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from samplehc import SampleHealthcare, AsyncSampleHealthcare
from tests.utils import assert_matches_type
from samplehc.types.api import (
    V1CreateSqlResponse,
    V1CreateAuditLogResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestV1:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_audit_log(self, client: SampleHealthcare) -> None:
        v1 = client.api.v1.create_audit_log(
            query="query",
        )
        assert_matches_type(V1CreateAuditLogResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_audit_log(self, client: SampleHealthcare) -> None:
        response = client.api.v1.with_raw_response.create_audit_log(
            query="query",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = response.parse()
        assert_matches_type(V1CreateAuditLogResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_audit_log(self, client: SampleHealthcare) -> None:
        with client.api.v1.with_streaming_response.create_audit_log(
            query="query",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = response.parse()
            assert_matches_type(V1CreateAuditLogResponse, v1, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_create_sql(self, client: SampleHealthcare) -> None:
        v1 = client.api.v1.create_sql(
            params=[{}],
            query="query",
        )
        assert_matches_type(V1CreateSqlResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_sql_with_all_params(self, client: SampleHealthcare) -> None:
        v1 = client.api.v1.create_sql(
            params=[{}],
            query="query",
            array_mode=True,
        )
        assert_matches_type(V1CreateSqlResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_sql(self, client: SampleHealthcare) -> None:
        response = client.api.v1.with_raw_response.create_sql(
            params=[{}],
            query="query",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = response.parse()
        assert_matches_type(V1CreateSqlResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_sql(self, client: SampleHealthcare) -> None:
        with client.api.v1.with_streaming_response.create_sql(
            params=[{}],
            query="query",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = response.parse()
            assert_matches_type(V1CreateSqlResponse, v1, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncV1:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_audit_log(self, async_client: AsyncSampleHealthcare) -> None:
        v1 = await async_client.api.v1.create_audit_log(
            query="query",
        )
        assert_matches_type(V1CreateAuditLogResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_audit_log(self, async_client: AsyncSampleHealthcare) -> None:
        response = await async_client.api.v1.with_raw_response.create_audit_log(
            query="query",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = await response.parse()
        assert_matches_type(V1CreateAuditLogResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_audit_log(self, async_client: AsyncSampleHealthcare) -> None:
        async with async_client.api.v1.with_streaming_response.create_audit_log(
            query="query",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = await response.parse()
            assert_matches_type(V1CreateAuditLogResponse, v1, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_sql(self, async_client: AsyncSampleHealthcare) -> None:
        v1 = await async_client.api.v1.create_sql(
            params=[{}],
            query="query",
        )
        assert_matches_type(V1CreateSqlResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_sql_with_all_params(self, async_client: AsyncSampleHealthcare) -> None:
        v1 = await async_client.api.v1.create_sql(
            params=[{}],
            query="query",
            array_mode=True,
        )
        assert_matches_type(V1CreateSqlResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_sql(self, async_client: AsyncSampleHealthcare) -> None:
        response = await async_client.api.v1.with_raw_response.create_sql(
            params=[{}],
            query="query",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        v1 = await response.parse()
        assert_matches_type(V1CreateSqlResponse, v1, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_sql(self, async_client: AsyncSampleHealthcare) -> None:
        async with async_client.api.v1.with_streaming_response.create_sql(
            params=[{}],
            query="query",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            v1 = await response.parse()
            assert_matches_type(V1CreateSqlResponse, v1, path=["response"])

        assert cast(Any, response.is_closed) is True
