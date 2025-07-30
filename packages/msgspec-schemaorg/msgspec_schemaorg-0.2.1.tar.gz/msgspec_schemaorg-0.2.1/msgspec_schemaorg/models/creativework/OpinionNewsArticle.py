from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.NewsArticle import NewsArticle
from typing import Optional, Union, Dict, List, Any


class OpinionNewsArticle(NewsArticle):
    """An [[OpinionNewsArticle]] is a [[NewsArticle]] that primarily expresses opinions rather than journalistic reporting of news and events. For example, a [[NewsArticle]] consisting of a column or [[Blog]]/[[BlogPosting]] entry in the Opinions section of a news publication. """
    type: str = field(default_factory=lambda: "OpinionNewsArticle", name="@type")