from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.LearningResource import LearningResource
from typing import Optional, Union, Dict, List, Any


class Quiz(LearningResource):
    """Quiz: A test of knowledge, skills and abilities."""
    type: str = field(default_factory=lambda: "Quiz", name="@type")