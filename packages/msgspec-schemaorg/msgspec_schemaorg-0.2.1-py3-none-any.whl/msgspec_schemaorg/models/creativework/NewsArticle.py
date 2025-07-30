from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.Article import Article
from typing import Optional, Union, Dict, List, Any


class NewsArticle(Article):
    """A NewsArticle is an article whose content reports news, or provides background context and supporting materials for understanding the news.

A more detailed overview of [schema.org News markup](/docs/news.html) is also available.
"""
    type: str = field(default_factory=lambda: "NewsArticle", name="@type")
    printColumn: Union[List[str], str, None] = None
    printSection: Union[List[str], str, None] = None
    printPage: Union[List[str], str, None] = None
    printEdition: Union[List[str], str, None] = None
    dateline: Union[List[str], str, None] = None