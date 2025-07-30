from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.WebPage import WebPage
from typing import Optional, Union, Dict, List, Any


class QAPage(WebPage):
    """A QAPage is a WebPage focussed on a specific Question and its Answer(s), e.g. in a question answering site or documenting Frequently Asked Questions (FAQs)."""
    type: str = field(default_factory=lambda: "QAPage", name="@type")