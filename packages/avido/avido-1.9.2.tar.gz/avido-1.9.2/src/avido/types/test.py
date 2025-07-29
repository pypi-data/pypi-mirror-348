# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .eval import Eval
from .task import Task
from .._models import BaseModel

__all__ = ["Test"]


class Test(BaseModel):
    __test__ = False
    id: str
    """Unique identifier of the run"""

    created_at: str = FieldInfo(alias="createdAt")
    """When the run was created"""

    evals: List[Eval]
    """Array of evaluations in this run"""

    modified_at: str = FieldInfo(alias="modifiedAt")
    """When the run was last modified"""

    status: Literal["PENDING", "IN_PROGRESS", "PASSED", "COMPLETED", "FAILED"]
    """Status of the evaluation/test.

    Valid options: PENDING, IN_PROGRESS, PASSED, COMPLETED, FAILED.
    """

    task: Task
    """
    A task that represents a specific job-to-be-done by the LLM in the user
    application.
    """

    result: Optional[Literal["PASSED", "FAILED"]] = None
    """Result of the run (if completed)"""

    trace_id: Optional[str] = FieldInfo(alias="traceId", default=None)
    """Optional ID of the trace this run is associated with"""
