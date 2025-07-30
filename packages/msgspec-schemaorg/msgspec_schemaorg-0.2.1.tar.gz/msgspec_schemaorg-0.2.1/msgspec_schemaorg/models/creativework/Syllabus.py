from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.LearningResource import LearningResource
from typing import Optional, Union, Dict, List, Any


class Syllabus(LearningResource):
    """A syllabus that describes the material covered in a course, often with several such sections per [[Course]] so that a distinct [[timeRequired]] can be provided for that section of the [[Course]]."""
    type: str = field(default_factory=lambda: "Syllabus", name="@type")