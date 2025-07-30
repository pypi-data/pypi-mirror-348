from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.BioChemEntity import BioChemEntity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.thing.AnatomicalStructure import AnatomicalStructure
    from msgspec_schemaorg.models.thing.AnatomicalSystem import AnatomicalSystem
    from msgspec_schemaorg.models.thing.BioChemEntity import BioChemEntity
    from msgspec_schemaorg.models.thing.Gene import Gene
from typing import Optional, Union, Dict, List, Any


class Gene(BioChemEntity):
    """A discrete unit of inheritance which affects one or more biological traits (Source: [https://en.wikipedia.org/wiki/Gene](https://en.wikipedia.org/wiki/Gene)). Examples include FOXP2 (Forkhead box protein P2), SCARNA21 (small Cajal body-specific RNA 21), A- (agouti genotype)."""
    type: str = field(default_factory=lambda: "Gene", name="@type")
    encodesBioChemEntity: Union[List['BioChemEntity'], 'BioChemEntity', None] = None
    expressedIn: Union[List[Union['AnatomicalStructure', 'DefinedTerm', 'BioChemEntity', 'AnatomicalSystem']], Union['AnatomicalStructure', 'DefinedTerm', 'BioChemEntity', 'AnatomicalSystem'], None] = None
    alternativeOf: Union[List['Gene'], 'Gene', None] = None
    hasBioPolymerSequence: Union[List[str], str, None] = None