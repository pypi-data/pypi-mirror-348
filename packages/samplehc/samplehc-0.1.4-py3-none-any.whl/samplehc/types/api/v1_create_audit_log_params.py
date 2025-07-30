# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["V1CreateAuditLogParams"]


class V1CreateAuditLogParams(TypedDict, total=False):
    query: Required[str]
    """The query string to filter audit logs."""
