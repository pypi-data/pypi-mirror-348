from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.Comment import Comment
from typing import Optional, Union, Dict, List, Any


class CorrectionComment(Comment):
    """A [[comment]] that corrects [[CreativeWork]]."""
    type: str = field(default_factory=lambda: "CorrectionComment", name="@type")