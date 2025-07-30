from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.Thing import Thing
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.Grant import Grant
    from msgspec_schemaorg.models.intangible.PropertyValue import PropertyValue
    from msgspec_schemaorg.models.thing.BioChemEntity import BioChemEntity
    from msgspec_schemaorg.models.thing.Gene import Gene
    from msgspec_schemaorg.models.thing.MedicalCondition import MedicalCondition
    from msgspec_schemaorg.models.thing.Taxon import Taxon
from typing import Optional, Union, Dict, List, Any


class BioChemEntity(Thing):
    """Any biological, chemical, or biochemical thing. For example: a protein; a gene; a chemical; a synthetic chemical."""
    type: str = field(default_factory=lambda: "BioChemEntity", name="@type")
    taxonomicRange: Union[List[Union['URL', str, 'Taxon', 'DefinedTerm']], Union['URL', str, 'Taxon', 'DefinedTerm'], None] = None
    hasBioChemEntityPart: Union[List['BioChemEntity'], 'BioChemEntity', None] = None
    associatedDisease: Union[List[Union['URL', 'PropertyValue', 'MedicalCondition']], Union['URL', 'PropertyValue', 'MedicalCondition'], None] = None
    funding: Union[List['Grant'], 'Grant', None] = None
    bioChemInteraction: Union[List['BioChemEntity'], 'BioChemEntity', None] = None
    isEncodedByBioChemEntity: Union[List['Gene'], 'Gene', None] = None
    isInvolvedInBiologicalProcess: Union[List[Union['URL', 'PropertyValue', 'DefinedTerm']], Union['URL', 'PropertyValue', 'DefinedTerm'], None] = None
    hasMolecularFunction: Union[List[Union['URL', 'DefinedTerm', 'PropertyValue']], Union['URL', 'DefinedTerm', 'PropertyValue'], None] = None
    biologicalRole: Union[List['DefinedTerm'], 'DefinedTerm', None] = None
    bioChemSimilarity: Union[List['BioChemEntity'], 'BioChemEntity', None] = None
    hasRepresentation: Union[List[Union['URL', str, 'PropertyValue']], Union['URL', str, 'PropertyValue'], None] = None
    isPartOfBioChemEntity: Union[List['BioChemEntity'], 'BioChemEntity', None] = None
    isLocatedInSubcellularLocation: Union[List[Union['URL', 'PropertyValue', 'DefinedTerm']], Union['URL', 'PropertyValue', 'DefinedTerm'], None] = None