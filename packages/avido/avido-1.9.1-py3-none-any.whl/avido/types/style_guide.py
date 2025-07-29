# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .application import Application

__all__ = ["StyleGuide", "Definition"]


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


class StyleGuide(BaseModel):
    id: str
    """The unique identifier of the style guide"""

    application: Application
    """Application configuration and metadata"""

    content: Dict[str, object]
    """The JSON content of the style guide"""

    created_at: str = FieldInfo(alias="createdAt")
    """The date and time the style guide was created"""

    definitions: List[Definition]

    modified_at: str = FieldInfo(alias="modifiedAt")
    """The date and time the style guide was last updated"""

    quickstart_id: Optional[str] = FieldInfo(alias="quickstartId", default=None)
    """The ID of the associated quickstart if any"""
