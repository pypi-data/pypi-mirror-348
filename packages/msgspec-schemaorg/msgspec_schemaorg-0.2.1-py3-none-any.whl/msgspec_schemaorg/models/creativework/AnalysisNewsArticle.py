from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.NewsArticle import NewsArticle
from typing import Optional, Union, Dict, List, Any


class AnalysisNewsArticle(NewsArticle):
    """An AnalysisNewsArticle is a [[NewsArticle]] that, while based on factual reporting, incorporates the expertise of the author/producer, offering interpretations and conclusions."""
    type: str = field(default_factory=lambda: "AnalysisNewsArticle", name="@type")