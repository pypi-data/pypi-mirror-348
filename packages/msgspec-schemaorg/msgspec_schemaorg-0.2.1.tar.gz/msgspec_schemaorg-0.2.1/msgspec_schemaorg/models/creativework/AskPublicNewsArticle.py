from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.NewsArticle import NewsArticle
from typing import Optional, Union, Dict, List, Any


class AskPublicNewsArticle(NewsArticle):
    """A [[NewsArticle]] expressing an open call by a [[NewsMediaOrganization]] asking the public for input, insights, clarifications, anecdotes, documentation, etc., on an issue, for reporting purposes."""
    type: str = field(default_factory=lambda: "AskPublicNewsArticle", name="@type")