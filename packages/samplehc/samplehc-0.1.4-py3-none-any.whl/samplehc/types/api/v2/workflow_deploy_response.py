# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["WorkflowDeployResponse"]


class WorkflowDeployResponse(BaseModel):
    workflow_deployment_id: str = FieldInfo(alias="workflowDeploymentId")
    """The ID of the newly created workflow deployment."""
