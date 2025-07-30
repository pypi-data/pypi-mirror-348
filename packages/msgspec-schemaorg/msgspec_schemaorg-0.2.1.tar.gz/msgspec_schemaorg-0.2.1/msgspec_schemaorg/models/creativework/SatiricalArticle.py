from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.Article import Article
from typing import Optional, Union, Dict, List, Any


class SatiricalArticle(Article):
    """An [[Article]] whose content is primarily [[satirical]](https://en.wikipedia.org/wiki/Satire) in nature, i.e. unlikely to be literally true. A satirical article is sometimes but not necessarily also a [[NewsArticle]]. [[ScholarlyArticle]]s are also sometimes satirized."""
    type: str = field(default_factory=lambda: "SatiricalArticle", name="@type")