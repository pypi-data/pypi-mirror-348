# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["LedgerCreateOrderParams"]


class LedgerCreateOrderParams(TypedDict, total=False):
    claim_amount: Required[Annotated[str, PropertyInfo(alias="claimAmount")]]
    """Total amount of the claim, in cents."""

    claim_id: Required[Annotated[str, PropertyInfo(alias="claimId")]]
    """Identifier of the claim associated with this ledger entry."""

    institution_amount: Required[Annotated[str, PropertyInfo(alias="institutionAmount")]]
    """Amount allocated to or from the institution, in cents."""

    institution_id: Required[Annotated[str, PropertyInfo(alias="institutionId")]]
    """Identifier of the financial institution involved."""

    insurance_id: Required[Annotated[str, PropertyInfo(alias="insuranceId")]]
    """Identifier of the insurance provider. Payments are often grouped by this ID."""

    order_id: Required[Annotated[str, PropertyInfo(alias="orderId")]]
    """Unique identifier for the order being processed."""

    patient_amount: Required[Annotated[str, PropertyInfo(alias="patientAmount")]]
    """Amount allocated to or from the patient, in cents."""

    patient_id: Required[Annotated[str, PropertyInfo(alias="patientId")]]
    """Identifier of the patient related to this ledger entry."""

    unallocated_amount: Required[Annotated[str, PropertyInfo(alias="unallocatedAmount")]]
    """Any portion of the order amount that remains unallocated, in cents."""
