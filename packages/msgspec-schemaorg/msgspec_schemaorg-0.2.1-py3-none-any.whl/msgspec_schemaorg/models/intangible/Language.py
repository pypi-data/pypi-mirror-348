from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import Optional, Union, Dict, List, Any


class Language(Intangible):
    """Natural languages such as Spanish, Tamil, Hindi, English, etc. Formal language code tags expressed in [BCP 47](https://en.wikipedia.org/wiki/IETF_language_tag) can be used via the [[alternateName]] property. The Language type previously also covered programming languages such as Scheme and Lisp, which are now best represented using [[ComputerLanguage]]."""
    type: str = field(default_factory=lambda: "Language", name="@type")