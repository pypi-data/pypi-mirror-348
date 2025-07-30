from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.NewsArticle import NewsArticle
from typing import Optional, Union, Dict, List, Any


class ReviewNewsArticle(NewsArticle):
    """A [[NewsArticle]] and [[CriticReview]] providing a professional critic's assessment of a service, product, performance, or artistic or literary work."""
    type: str = field(default_factory=lambda: "ReviewNewsArticle", name="@type")