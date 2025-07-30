from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.Article import Article
from typing import Optional, Union, Dict, List, Any


class ScholarlyArticle(Article):
    """A scholarly article."""
    type: str = field(default_factory=lambda: "ScholarlyArticle", name="@type")