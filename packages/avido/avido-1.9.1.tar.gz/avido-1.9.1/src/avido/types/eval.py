# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .application import Application

__all__ = ["Eval", "Definition"]


class Definition(BaseModel):
    id: str

    created_at: str = FieldInfo(alias="createdAt")

    modified_at: str = FieldInfo(alias="modifiedAt")

    name: str

    type: Literal["NATURALNESS", "STYLE", "RECALL", "CUSTOM", "BLACKLIST", "FACT"]
    """Type of evaluation. Valid options: NATURALNESS, STYLE, RECALL, CUSTOM, FACT."""

    application: Optional[Application] = None
    """Application configuration and metadata"""

    global_config: Optional[object] = FieldInfo(alias="globalConfig", default=None)

    style_guide_id: Optional[str] = FieldInfo(alias="styleGuideId", default=None)


class Eval(BaseModel):
    id: str
    """Unique identifier of the evaluation"""

    created_at: str = FieldInfo(alias="createdAt")
    """When the evaluation was created"""

    definition: Definition

    modified_at: str = FieldInfo(alias="modifiedAt")
    """When the evaluation was last modified"""

    org_id: str = FieldInfo(alias="orgId")
    """Organization ID that owns this evaluation"""

    status: Literal["PENDING", "IN_PROGRESS", "PASSED", "COMPLETED", "FAILED"]
    """Status of the evaluation/test.

    Valid options: PENDING, IN_PROGRESS, PASSED, COMPLETED, FAILED.
    """

    results: Optional[object] = None
    """Results of the evaluation (structure depends on eval type)."""
