from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.DefinedTermSet import DefinedTermSet
from typing import Optional, Union, Dict, List, Any


class DefinedTerm(Intangible):
    """A word, name, acronym, phrase, etc. with a formal definition. Often used in the context of category or subject classification, glossaries or dictionaries, product or creative work types, etc. Use the name property for the term being defined, use termCode if the term has an alpha-numeric code allocated, use description to provide the definition of the term."""
    type: str = field(default_factory=lambda: "DefinedTerm", name="@type")
    inDefinedTermSet: Union[List[Union['URL', 'DefinedTermSet']], Union['URL', 'DefinedTermSet'], None] = None
    termCode: Union[List[str], str, None] = None