# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import maybe_transform, async_maybe_transform
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.api.v2 import (
    ledger_create_order_params,
    ledger_post_claim_payment_params,
    ledger_post_order_writeoff_params,
    ledger_post_patient_payment_params,
    ledger_post_claim_adjustment_params,
    ledger_post_institution_payment_params,
    ledger_create_patient_adjustment_params,
    ledger_post_institution_adjustment_params,
)
from ....types.api.v2.ledger_create_order_response import LedgerCreateOrderResponse
from ....types.api.v2.ledger_post_claim_payment_response import LedgerPostClaimPaymentResponse
from ....types.api.v2.ledger_post_order_writeoff_response import LedgerPostOrderWriteoffResponse
from ....types.api.v2.ledger_post_patient_payment_response import LedgerPostPatientPaymentResponse
from ....types.api.v2.ledger_post_claim_adjustment_response import LedgerPostClaimAdjustmentResponse
from ....types.api.v2.ledger_post_institution_payment_response import LedgerPostInstitutionPaymentResponse
from ....types.api.v2.ledger_create_patient_adjustment_response import LedgerCreatePatientAdjustmentResponse
from ....types.api.v2.ledger_post_institution_adjustment_response import LedgerPostInstitutionAdjustmentResponse

__all__ = ["LedgerResource", "AsyncLedgerResource"]


class LedgerResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> LedgerResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/samplehc/samplehc-python#accessing-raw-response-data-eg-headers
        """
        return LedgerResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> LedgerResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/samplehc/samplehc-python#with_streaming_response
        """
        return LedgerResourceWithStreamingResponse(self)

    def create_order(
        self,
        *,
        claim_amount_usd_cents: float,
        institution_amount_usd_cents: float,
        order_id: str,
        patient_amount_usd_cents: float,
        patient_id: str,
        unallocated_amount_usd_cents: float,
        claim_id: str | NotGiven = NOT_GIVEN,
        institution_id: str | NotGiven = NOT_GIVEN,
        insurance_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LedgerCreateOrderResponse:
        """
        Creates a new ledger entry for an order, linking claim, institution, patient,
        and insurance financial details. All monetary amounts should be provided in
        cents.

        Args:
          claim_amount_usd_cents: Total amount of the claim, in cents.

          institution_amount_usd_cents: Amount allocated to or from the institution, in cents.

          order_id: Unique identifier for the order being processed.

          patient_amount_usd_cents: Amount allocated to or from the patient, in cents.

          patient_id: Identifier of the patient related to this ledger entry.

          unallocated_amount_usd_cents: Any portion of the order amount that remains unallocated, in cents.

          claim_id: Identifier of the claim associated with this ledger entry.

          institution_id: Identifier of the financial institution involved.

          insurance_id: Identifier of the insurance provider. Payments are often grouped by this ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/ledger/new-order",
            body=maybe_transform(
                {
                    "claim_amount_usd_cents": claim_amount_usd_cents,
                    "institution_amount_usd_cents": institution_amount_usd_cents,
                    "order_id": order_id,
                    "patient_amount_usd_cents": patient_amount_usd_cents,
                    "patient_id": patient_id,
                    "unallocated_amount_usd_cents": unallocated_amount_usd_cents,
                    "claim_id": claim_id,
                    "institution_id": institution_id,
                    "insurance_id": insurance_id,
                },
                ledger_create_order_params.LedgerCreateOrderParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LedgerCreateOrderResponse,
        )

    def create_patient_adjustment(
        self,
        *,
        amount_usd_cents: float,
        ik: str,
        order_id: str,
        patient_id: str,
        reason: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LedgerCreatePatientAdjustmentResponse:
        """Posts a patient adjustment to the ledger.

        All monetary amounts should be
        provided in cents.

        Args:
          amount_usd_cents: Adjustment amount in cents (positive or negative).

          ik: Idempotency key for the adjustment.

          order_id: Order ID associated with the adjustment.

          patient_id: Identifier of the patient for the adjustment.

          reason: Reason for the adjustment.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/ledger/patient-adjustment",
            body=maybe_transform(
                {
                    "amount_usd_cents": amount_usd_cents,
                    "ik": ik,
                    "order_id": order_id,
                    "patient_id": patient_id,
                    "reason": reason,
                },
                ledger_create_patient_adjustment_params.LedgerCreatePatientAdjustmentParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LedgerCreatePatientAdjustmentResponse,
        )

    def post_claim_adjustment(
        self,
        *,
        amount_usd_cents: float,
        claim_id: str,
        ik: str,
        insurance_id: str,
        order_id: str,
        reason: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LedgerPostClaimAdjustmentResponse:
        """Posts a claim adjustment to the ledger.

        All monetary amounts should be provided
        in cents.

        Args:
          amount_usd_cents: Adjustment amount in cents (positive or negative).

          claim_id: Identifier of the claim associated with this adjustment.

          ik: Idempotency key for the adjustment.

          insurance_id: Identifier of the insurance for the adjustment.

          order_id: Order ID associated with the adjustment.

          reason: Reason for the adjustment.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/ledger/claim-adjustment",
            body=maybe_transform(
                {
                    "amount_usd_cents": amount_usd_cents,
                    "claim_id": claim_id,
                    "ik": ik,
                    "insurance_id": insurance_id,
                    "order_id": order_id,
                    "reason": reason,
                },
                ledger_post_claim_adjustment_params.LedgerPostClaimAdjustmentParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LedgerPostClaimAdjustmentResponse,
        )

    def post_claim_payment(
        self,
        *,
        amount_usd_cents: float,
        claim_id: str,
        ik: str,
        insurance_id: str,
        order_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LedgerPostClaimPaymentResponse:
        """Posts a claim payment to the ledger.

        All monetary amounts should be provided in
        cents.

        Args:
          amount_usd_cents: Payment amount in cents.

          claim_id: Identifier of the claim associated with this payment.

          ik: Idempotency key for the payment.

          insurance_id: Identifier of the insurance for the payment.

          order_id: Order ID associated with the payment.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/ledger/claim-payment",
            body=maybe_transform(
                {
                    "amount_usd_cents": amount_usd_cents,
                    "claim_id": claim_id,
                    "ik": ik,
                    "insurance_id": insurance_id,
                    "order_id": order_id,
                },
                ledger_post_claim_payment_params.LedgerPostClaimPaymentParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LedgerPostClaimPaymentResponse,
        )

    def post_institution_adjustment(
        self,
        *,
        amount_usd_cents: float,
        claim_id: str,
        ik: str,
        institution_id: str,
        order_id: str,
        reason: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LedgerPostInstitutionAdjustmentResponse:
        """Posts an institution adjustment to the ledger.

        All monetary amounts should be
        provided in cents.

        Args:
          amount_usd_cents: Adjustment amount in cents (positive or negative).

          claim_id: Identifier of the claim associated with this adjustment.

          ik: Idempotency key for the adjustment.

          institution_id: Identifier of the institution for the adjustment.

          order_id: Order ID associated with the adjustment.

          reason: Reason for the adjustment.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/ledger/institution-adjustment",
            body=maybe_transform(
                {
                    "amount_usd_cents": amount_usd_cents,
                    "claim_id": claim_id,
                    "ik": ik,
                    "institution_id": institution_id,
                    "order_id": order_id,
                    "reason": reason,
                },
                ledger_post_institution_adjustment_params.LedgerPostInstitutionAdjustmentParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LedgerPostInstitutionAdjustmentResponse,
        )

    def post_institution_payment(
        self,
        *,
        amount_usd_cents: float,
        claim_id: str,
        ik: str,
        institution_id: str,
        order_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LedgerPostInstitutionPaymentResponse:
        """Posts an institution payment to the ledger.

        All monetary amounts should be
        provided in cents.

        Args:
          amount_usd_cents: Payment amount in cents.

          claim_id: Identifier of the claim associated with this payment.

          ik: Idempotency key for the payment.

          institution_id: Identifier of the institution for the payment.

          order_id: Order ID associated with the payment.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/ledger/institution-payment",
            body=maybe_transform(
                {
                    "amount_usd_cents": amount_usd_cents,
                    "claim_id": claim_id,
                    "ik": ik,
                    "institution_id": institution_id,
                    "order_id": order_id,
                },
                ledger_post_institution_payment_params.LedgerPostInstitutionPaymentParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LedgerPostInstitutionPaymentResponse,
        )

    def post_order_writeoff(
        self,
        *,
        amount_usd_cents: float,
        ik: str,
        order_id: str,
        reason: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LedgerPostOrderWriteoffResponse:
        """Posts an order write-off to the ledger.

        All monetary amounts should be provided
        in cents.

        Args:
          amount_usd_cents: Write-off amount in cents.

          ik: Idempotency key for the write-off.

          order_id: Order ID associated with the write-off.

          reason: Reason for the write-off.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/ledger/order-writeoff",
            body=maybe_transform(
                {
                    "amount_usd_cents": amount_usd_cents,
                    "ik": ik,
                    "order_id": order_id,
                    "reason": reason,
                },
                ledger_post_order_writeoff_params.LedgerPostOrderWriteoffParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LedgerPostOrderWriteoffResponse,
        )

    def post_patient_payment(
        self,
        *,
        amount_usd_cents: float,
        ik: str,
        order_id: str,
        patient_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LedgerPostPatientPaymentResponse:
        """Posts a patient payment to the ledger.

        All monetary amounts should be provided
        in cents.

        Args:
          amount_usd_cents: Payment amount in cents.

          ik: Idempotency key for the payment.

          order_id: Order ID associated with the payment.

          patient_id: Identifier of the patient for the payment.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/ledger/patient-payment",
            body=maybe_transform(
                {
                    "amount_usd_cents": amount_usd_cents,
                    "ik": ik,
                    "order_id": order_id,
                    "patient_id": patient_id,
                },
                ledger_post_patient_payment_params.LedgerPostPatientPaymentParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LedgerPostPatientPaymentResponse,
        )


class AsyncLedgerResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncLedgerResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/samplehc/samplehc-python#accessing-raw-response-data-eg-headers
        """
        return AsyncLedgerResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncLedgerResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/samplehc/samplehc-python#with_streaming_response
        """
        return AsyncLedgerResourceWithStreamingResponse(self)

    async def create_order(
        self,
        *,
        claim_amount_usd_cents: float,
        institution_amount_usd_cents: float,
        order_id: str,
        patient_amount_usd_cents: float,
        patient_id: str,
        unallocated_amount_usd_cents: float,
        claim_id: str | NotGiven = NOT_GIVEN,
        institution_id: str | NotGiven = NOT_GIVEN,
        insurance_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LedgerCreateOrderResponse:
        """
        Creates a new ledger entry for an order, linking claim, institution, patient,
        and insurance financial details. All monetary amounts should be provided in
        cents.

        Args:
          claim_amount_usd_cents: Total amount of the claim, in cents.

          institution_amount_usd_cents: Amount allocated to or from the institution, in cents.

          order_id: Unique identifier for the order being processed.

          patient_amount_usd_cents: Amount allocated to or from the patient, in cents.

          patient_id: Identifier of the patient related to this ledger entry.

          unallocated_amount_usd_cents: Any portion of the order amount that remains unallocated, in cents.

          claim_id: Identifier of the claim associated with this ledger entry.

          institution_id: Identifier of the financial institution involved.

          insurance_id: Identifier of the insurance provider. Payments are often grouped by this ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/ledger/new-order",
            body=await async_maybe_transform(
                {
                    "claim_amount_usd_cents": claim_amount_usd_cents,
                    "institution_amount_usd_cents": institution_amount_usd_cents,
                    "order_id": order_id,
                    "patient_amount_usd_cents": patient_amount_usd_cents,
                    "patient_id": patient_id,
                    "unallocated_amount_usd_cents": unallocated_amount_usd_cents,
                    "claim_id": claim_id,
                    "institution_id": institution_id,
                    "insurance_id": insurance_id,
                },
                ledger_create_order_params.LedgerCreateOrderParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LedgerCreateOrderResponse,
        )

    async def create_patient_adjustment(
        self,
        *,
        amount_usd_cents: float,
        ik: str,
        order_id: str,
        patient_id: str,
        reason: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LedgerCreatePatientAdjustmentResponse:
        """Posts a patient adjustment to the ledger.

        All monetary amounts should be
        provided in cents.

        Args:
          amount_usd_cents: Adjustment amount in cents (positive or negative).

          ik: Idempotency key for the adjustment.

          order_id: Order ID associated with the adjustment.

          patient_id: Identifier of the patient for the adjustment.

          reason: Reason for the adjustment.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/ledger/patient-adjustment",
            body=await async_maybe_transform(
                {
                    "amount_usd_cents": amount_usd_cents,
                    "ik": ik,
                    "order_id": order_id,
                    "patient_id": patient_id,
                    "reason": reason,
                },
                ledger_create_patient_adjustment_params.LedgerCreatePatientAdjustmentParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LedgerCreatePatientAdjustmentResponse,
        )

    async def post_claim_adjustment(
        self,
        *,
        amount_usd_cents: float,
        claim_id: str,
        ik: str,
        insurance_id: str,
        order_id: str,
        reason: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LedgerPostClaimAdjustmentResponse:
        """Posts a claim adjustment to the ledger.

        All monetary amounts should be provided
        in cents.

        Args:
          amount_usd_cents: Adjustment amount in cents (positive or negative).

          claim_id: Identifier of the claim associated with this adjustment.

          ik: Idempotency key for the adjustment.

          insurance_id: Identifier of the insurance for the adjustment.

          order_id: Order ID associated with the adjustment.

          reason: Reason for the adjustment.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/ledger/claim-adjustment",
            body=await async_maybe_transform(
                {
                    "amount_usd_cents": amount_usd_cents,
                    "claim_id": claim_id,
                    "ik": ik,
                    "insurance_id": insurance_id,
                    "order_id": order_id,
                    "reason": reason,
                },
                ledger_post_claim_adjustment_params.LedgerPostClaimAdjustmentParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LedgerPostClaimAdjustmentResponse,
        )

    async def post_claim_payment(
        self,
        *,
        amount_usd_cents: float,
        claim_id: str,
        ik: str,
        insurance_id: str,
        order_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LedgerPostClaimPaymentResponse:
        """Posts a claim payment to the ledger.

        All monetary amounts should be provided in
        cents.

        Args:
          amount_usd_cents: Payment amount in cents.

          claim_id: Identifier of the claim associated with this payment.

          ik: Idempotency key for the payment.

          insurance_id: Identifier of the insurance for the payment.

          order_id: Order ID associated with the payment.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/ledger/claim-payment",
            body=await async_maybe_transform(
                {
                    "amount_usd_cents": amount_usd_cents,
                    "claim_id": claim_id,
                    "ik": ik,
                    "insurance_id": insurance_id,
                    "order_id": order_id,
                },
                ledger_post_claim_payment_params.LedgerPostClaimPaymentParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LedgerPostClaimPaymentResponse,
        )

    async def post_institution_adjustment(
        self,
        *,
        amount_usd_cents: float,
        claim_id: str,
        ik: str,
        institution_id: str,
        order_id: str,
        reason: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LedgerPostInstitutionAdjustmentResponse:
        """Posts an institution adjustment to the ledger.

        All monetary amounts should be
        provided in cents.

        Args:
          amount_usd_cents: Adjustment amount in cents (positive or negative).

          claim_id: Identifier of the claim associated with this adjustment.

          ik: Idempotency key for the adjustment.

          institution_id: Identifier of the institution for the adjustment.

          order_id: Order ID associated with the adjustment.

          reason: Reason for the adjustment.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/ledger/institution-adjustment",
            body=await async_maybe_transform(
                {
                    "amount_usd_cents": amount_usd_cents,
                    "claim_id": claim_id,
                    "ik": ik,
                    "institution_id": institution_id,
                    "order_id": order_id,
                    "reason": reason,
                },
                ledger_post_institution_adjustment_params.LedgerPostInstitutionAdjustmentParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LedgerPostInstitutionAdjustmentResponse,
        )

    async def post_institution_payment(
        self,
        *,
        amount_usd_cents: float,
        claim_id: str,
        ik: str,
        institution_id: str,
        order_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LedgerPostInstitutionPaymentResponse:
        """Posts an institution payment to the ledger.

        All monetary amounts should be
        provided in cents.

        Args:
          amount_usd_cents: Payment amount in cents.

          claim_id: Identifier of the claim associated with this payment.

          ik: Idempotency key for the payment.

          institution_id: Identifier of the institution for the payment.

          order_id: Order ID associated with the payment.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/ledger/institution-payment",
            body=await async_maybe_transform(
                {
                    "amount_usd_cents": amount_usd_cents,
                    "claim_id": claim_id,
                    "ik": ik,
                    "institution_id": institution_id,
                    "order_id": order_id,
                },
                ledger_post_institution_payment_params.LedgerPostInstitutionPaymentParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LedgerPostInstitutionPaymentResponse,
        )

    async def post_order_writeoff(
        self,
        *,
        amount_usd_cents: float,
        ik: str,
        order_id: str,
        reason: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LedgerPostOrderWriteoffResponse:
        """Posts an order write-off to the ledger.

        All monetary amounts should be provided
        in cents.

        Args:
          amount_usd_cents: Write-off amount in cents.

          ik: Idempotency key for the write-off.

          order_id: Order ID associated with the write-off.

          reason: Reason for the write-off.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/ledger/order-writeoff",
            body=await async_maybe_transform(
                {
                    "amount_usd_cents": amount_usd_cents,
                    "ik": ik,
                    "order_id": order_id,
                    "reason": reason,
                },
                ledger_post_order_writeoff_params.LedgerPostOrderWriteoffParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LedgerPostOrderWriteoffResponse,
        )

    async def post_patient_payment(
        self,
        *,
        amount_usd_cents: float,
        ik: str,
        order_id: str,
        patient_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LedgerPostPatientPaymentResponse:
        """Posts a patient payment to the ledger.

        All monetary amounts should be provided
        in cents.

        Args:
          amount_usd_cents: Payment amount in cents.

          ik: Idempotency key for the payment.

          order_id: Order ID associated with the payment.

          patient_id: Identifier of the patient for the payment.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/ledger/patient-payment",
            body=await async_maybe_transform(
                {
                    "amount_usd_cents": amount_usd_cents,
                    "ik": ik,
                    "order_id": order_id,
                    "patient_id": patient_id,
                },
                ledger_post_patient_payment_params.LedgerPostPatientPaymentParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LedgerPostPatientPaymentResponse,
        )


class LedgerResourceWithRawResponse:
    def __init__(self, ledger: LedgerResource) -> None:
        self._ledger = ledger

        self.create_order = to_raw_response_wrapper(
            ledger.create_order,
        )
        self.create_patient_adjustment = to_raw_response_wrapper(
            ledger.create_patient_adjustment,
        )
        self.post_claim_adjustment = to_raw_response_wrapper(
            ledger.post_claim_adjustment,
        )
        self.post_claim_payment = to_raw_response_wrapper(
            ledger.post_claim_payment,
        )
        self.post_institution_adjustment = to_raw_response_wrapper(
            ledger.post_institution_adjustment,
        )
        self.post_institution_payment = to_raw_response_wrapper(
            ledger.post_institution_payment,
        )
        self.post_order_writeoff = to_raw_response_wrapper(
            ledger.post_order_writeoff,
        )
        self.post_patient_payment = to_raw_response_wrapper(
            ledger.post_patient_payment,
        )


class AsyncLedgerResourceWithRawResponse:
    def __init__(self, ledger: AsyncLedgerResource) -> None:
        self._ledger = ledger

        self.create_order = async_to_raw_response_wrapper(
            ledger.create_order,
        )
        self.create_patient_adjustment = async_to_raw_response_wrapper(
            ledger.create_patient_adjustment,
        )
        self.post_claim_adjustment = async_to_raw_response_wrapper(
            ledger.post_claim_adjustment,
        )
        self.post_claim_payment = async_to_raw_response_wrapper(
            ledger.post_claim_payment,
        )
        self.post_institution_adjustment = async_to_raw_response_wrapper(
            ledger.post_institution_adjustment,
        )
        self.post_institution_payment = async_to_raw_response_wrapper(
            ledger.post_institution_payment,
        )
        self.post_order_writeoff = async_to_raw_response_wrapper(
            ledger.post_order_writeoff,
        )
        self.post_patient_payment = async_to_raw_response_wrapper(
            ledger.post_patient_payment,
        )


class LedgerResourceWithStreamingResponse:
    def __init__(self, ledger: LedgerResource) -> None:
        self._ledger = ledger

        self.create_order = to_streamed_response_wrapper(
            ledger.create_order,
        )
        self.create_patient_adjustment = to_streamed_response_wrapper(
            ledger.create_patient_adjustment,
        )
        self.post_claim_adjustment = to_streamed_response_wrapper(
            ledger.post_claim_adjustment,
        )
        self.post_claim_payment = to_streamed_response_wrapper(
            ledger.post_claim_payment,
        )
        self.post_institution_adjustment = to_streamed_response_wrapper(
            ledger.post_institution_adjustment,
        )
        self.post_institution_payment = to_streamed_response_wrapper(
            ledger.post_institution_payment,
        )
        self.post_order_writeoff = to_streamed_response_wrapper(
            ledger.post_order_writeoff,
        )
        self.post_patient_payment = to_streamed_response_wrapper(
            ledger.post_patient_payment,
        )


class AsyncLedgerResourceWithStreamingResponse:
    def __init__(self, ledger: AsyncLedgerResource) -> None:
        self._ledger = ledger

        self.create_order = async_to_streamed_response_wrapper(
            ledger.create_order,
        )
        self.create_patient_adjustment = async_to_streamed_response_wrapper(
            ledger.create_patient_adjustment,
        )
        self.post_claim_adjustment = async_to_streamed_response_wrapper(
            ledger.post_claim_adjustment,
        )
        self.post_claim_payment = async_to_streamed_response_wrapper(
            ledger.post_claim_payment,
        )
        self.post_institution_adjustment = async_to_streamed_response_wrapper(
            ledger.post_institution_adjustment,
        )
        self.post_institution_payment = async_to_streamed_response_wrapper(
            ledger.post_institution_payment,
        )
        self.post_order_writeoff = async_to_streamed_response_wrapper(
            ledger.post_order_writeoff,
        )
        self.post_patient_payment = async_to_streamed_response_wrapper(
            ledger.post_patient_payment,
        )
