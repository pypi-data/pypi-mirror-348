from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.Article import Article
from typing import Optional, Union, Dict, List, Any


class TechArticle(Article):
    """A technical article - Example: How-to (task) topics, step-by-step, procedural troubleshooting, specifications, etc."""
    type: str = field(default_factory=lambda: "TechArticle", name="@type")
    proficiencyLevel: Union[List[str], str, None] = None
    dependencies: Union[List[str], str, None] = None