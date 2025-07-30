from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.BioChemEntity import BioChemEntity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from typing import Optional, Union, Dict, List, Any


class MolecularEntity(BioChemEntity):
    """Any constitutionally or isotopically distinct atom, molecule, ion, ion pair, radical, radical ion, complex, conformer etc., identifiable as a separately distinguishable entity."""
    type: str = field(default_factory=lambda: "MolecularEntity", name="@type")
    inChIKey: Union[List[str], str, None] = None
    molecularWeight: Union[List[Union[str, 'QuantitativeValue']], Union[str, 'QuantitativeValue'], None] = None
    smiles: Union[List[str], str, None] = None
    molecularFormula: Union[List[str], str, None] = None
    potentialUse: Union[List['DefinedTerm'], 'DefinedTerm', None] = None
    iupacName: Union[List[str], str, None] = None
    chemicalRole: Union[List['DefinedTerm'], 'DefinedTerm', None] = None
    inChI: Union[List[str], str, None] = None
    monoisotopicMolecularWeight: Union[List[Union[str, 'QuantitativeValue']], Union[str, 'QuantitativeValue'], None] = None