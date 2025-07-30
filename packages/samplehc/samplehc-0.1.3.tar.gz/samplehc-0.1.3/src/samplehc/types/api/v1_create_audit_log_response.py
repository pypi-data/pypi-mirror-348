# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List

from ..._models import BaseModel

__all__ = ["V1CreateAuditLogResponse"]


class V1CreateAuditLogResponse(BaseModel):
    data: List[Dict[str, object]]
    """An array of audit log records matching the query."""
