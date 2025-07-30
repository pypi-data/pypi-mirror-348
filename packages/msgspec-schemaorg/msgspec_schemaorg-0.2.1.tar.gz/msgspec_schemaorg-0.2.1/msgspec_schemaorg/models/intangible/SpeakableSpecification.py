from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import Optional, Union, Dict, List, Any


class SpeakableSpecification(Intangible):
    """A SpeakableSpecification indicates (typically via [[xpath]] or [[cssSelector]]) sections of a document that are highlighted as particularly [[speakable]]. Instances of this type are expected to be used primarily as values of the [[speakable]] property."""
    type: str = field(default_factory=lambda: "SpeakableSpecification", name="@type")
    xpath: Union[List[str], str, None] = None
    cssSelector: Union[List[str], str, None] = None