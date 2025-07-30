from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.base import SchemaOrgBase
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Language import Language
from typing import Optional, Union, Dict, List, Any


class PronounceableText(SchemaOrgBase):
    """Data type: PronounceableText."""
    type: str = field(default_factory=lambda: "PronounceableText", name="@type")
    textValue: Union[List[str], str, None] = None
    phoneticText: Union[List[str], str, None] = None
    speechToTextMarkup: Union[List[str], str, None] = None
    inLanguage: Union[List[Union[str, 'Language']], Union[str, 'Language'], None] = None