# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from samplehc import SampleHealthcare, AsyncSampleHealthcare
from tests.utils import assert_matches_type
from samplehc.types.api.v2 import (
    LedgerCreateOrderResponse,
    LedgerCreatePatientAdjustmentResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestLedger:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_order(self, client: SampleHealthcare) -> None:
        ledger = client.api.v2.ledger.create_order(
            claim_amount_usd_cents=0,
            institution_amount_usd_cents=0,
            order_id="orderId",
            patient_amount_usd_cents=0,
            patient_id="patientId",
            unallocated_amount_usd_cents=0,
        )
        assert_matches_type(LedgerCreateOrderResponse, ledger, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_order_with_all_params(self, client: SampleHealthcare) -> None:
        ledger = client.api.v2.ledger.create_order(
            claim_amount_usd_cents=0,
            institution_amount_usd_cents=0,
            order_id="orderId",
            patient_amount_usd_cents=0,
            patient_id="patientId",
            unallocated_amount_usd_cents=0,
            claim_id="claimId",
            institution_id="institutionId",
            insurance_id="insuranceId",
        )
        assert_matches_type(LedgerCreateOrderResponse, ledger, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_order(self, client: SampleHealthcare) -> None:
        response = client.api.v2.ledger.with_raw_response.create_order(
            claim_amount_usd_cents=0,
            institution_amount_usd_cents=0,
            order_id="orderId",
            patient_amount_usd_cents=0,
            patient_id="patientId",
            unallocated_amount_usd_cents=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        ledger = response.parse()
        assert_matches_type(LedgerCreateOrderResponse, ledger, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_order(self, client: SampleHealthcare) -> None:
        with client.api.v2.ledger.with_streaming_response.create_order(
            claim_amount_usd_cents=0,
            institution_amount_usd_cents=0,
            order_id="orderId",
            patient_amount_usd_cents=0,
            patient_id="patientId",
            unallocated_amount_usd_cents=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            ledger = response.parse()
            assert_matches_type(LedgerCreateOrderResponse, ledger, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_create_patient_adjustment(self, client: SampleHealthcare) -> None:
        ledger = client.api.v2.ledger.create_patient_adjustment(
            amount_usd_cents=0,
            ik="ik",
            order_id="orderId",
            patient_id="patientId",
            reason="reason",
        )
        assert_matches_type(LedgerCreatePatientAdjustmentResponse, ledger, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_patient_adjustment(self, client: SampleHealthcare) -> None:
        response = client.api.v2.ledger.with_raw_response.create_patient_adjustment(
            amount_usd_cents=0,
            ik="ik",
            order_id="orderId",
            patient_id="patientId",
            reason="reason",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        ledger = response.parse()
        assert_matches_type(LedgerCreatePatientAdjustmentResponse, ledger, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_patient_adjustment(self, client: SampleHealthcare) -> None:
        with client.api.v2.ledger.with_streaming_response.create_patient_adjustment(
            amount_usd_cents=0,
            ik="ik",
            order_id="orderId",
            patient_id="patientId",
            reason="reason",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            ledger = response.parse()
            assert_matches_type(LedgerCreatePatientAdjustmentResponse, ledger, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncLedger:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_order(self, async_client: AsyncSampleHealthcare) -> None:
        ledger = await async_client.api.v2.ledger.create_order(
            claim_amount_usd_cents=0,
            institution_amount_usd_cents=0,
            order_id="orderId",
            patient_amount_usd_cents=0,
            patient_id="patientId",
            unallocated_amount_usd_cents=0,
        )
        assert_matches_type(LedgerCreateOrderResponse, ledger, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_order_with_all_params(self, async_client: AsyncSampleHealthcare) -> None:
        ledger = await async_client.api.v2.ledger.create_order(
            claim_amount_usd_cents=0,
            institution_amount_usd_cents=0,
            order_id="orderId",
            patient_amount_usd_cents=0,
            patient_id="patientId",
            unallocated_amount_usd_cents=0,
            claim_id="claimId",
            institution_id="institutionId",
            insurance_id="insuranceId",
        )
        assert_matches_type(LedgerCreateOrderResponse, ledger, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_order(self, async_client: AsyncSampleHealthcare) -> None:
        response = await async_client.api.v2.ledger.with_raw_response.create_order(
            claim_amount_usd_cents=0,
            institution_amount_usd_cents=0,
            order_id="orderId",
            patient_amount_usd_cents=0,
            patient_id="patientId",
            unallocated_amount_usd_cents=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        ledger = await response.parse()
        assert_matches_type(LedgerCreateOrderResponse, ledger, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_order(self, async_client: AsyncSampleHealthcare) -> None:
        async with async_client.api.v2.ledger.with_streaming_response.create_order(
            claim_amount_usd_cents=0,
            institution_amount_usd_cents=0,
            order_id="orderId",
            patient_amount_usd_cents=0,
            patient_id="patientId",
            unallocated_amount_usd_cents=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            ledger = await response.parse()
            assert_matches_type(LedgerCreateOrderResponse, ledger, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_patient_adjustment(self, async_client: AsyncSampleHealthcare) -> None:
        ledger = await async_client.api.v2.ledger.create_patient_adjustment(
            amount_usd_cents=0,
            ik="ik",
            order_id="orderId",
            patient_id="patientId",
            reason="reason",
        )
        assert_matches_type(LedgerCreatePatientAdjustmentResponse, ledger, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_patient_adjustment(self, async_client: AsyncSampleHealthcare) -> None:
        response = await async_client.api.v2.ledger.with_raw_response.create_patient_adjustment(
            amount_usd_cents=0,
            ik="ik",
            order_id="orderId",
            patient_id="patientId",
            reason="reason",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        ledger = await response.parse()
        assert_matches_type(LedgerCreatePatientAdjustmentResponse, ledger, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_patient_adjustment(self, async_client: AsyncSampleHealthcare) -> None:
        async with async_client.api.v2.ledger.with_streaming_response.create_patient_adjustment(
            amount_usd_cents=0,
            ik="ik",
            order_id="orderId",
            patient_id="patientId",
            reason="reason",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            ledger = await response.parse()
            assert_matches_type(LedgerCreatePatientAdjustmentResponse, ledger, path=["response"])

        assert cast(Any, response.is_closed) is True
