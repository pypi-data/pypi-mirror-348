from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.BioChemEntity import BioChemEntity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
from typing import Optional, Union, Dict, List, Any


class ChemicalSubstance(BioChemEntity):
    """A chemical substance is 'a portion of matter of constant composition, composed of molecular entities of the same type or of different types' (source: [ChEBI:59999](https://www.ebi.ac.uk/chebi/searchId.do?chebiId=59999))."""
    type: str = field(default_factory=lambda: "ChemicalSubstance", name="@type")
    potentialUse: Union[List['DefinedTerm'], 'DefinedTerm', None] = None
    chemicalComposition: Union[List[str], str, None] = None
    chemicalRole: Union[List['DefinedTerm'], 'DefinedTerm', None] = None