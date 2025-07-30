from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalEntity import MedicalEntity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.ImageObject import ImageObject
    from msgspec_schemaorg.models.thing.AnatomicalStructure import AnatomicalStructure
    from msgspec_schemaorg.models.thing.AnatomicalSystem import AnatomicalSystem
    from msgspec_schemaorg.models.thing.MedicalCondition import MedicalCondition
    from msgspec_schemaorg.models.thing.MedicalTherapy import MedicalTherapy
from typing import Optional, Union, Dict, List, Any


class AnatomicalStructure(MedicalEntity):
    """Any part of the human body, typically a component of an anatomical system. Organs, tissues, and cells are all anatomical structures."""
    type: str = field(default_factory=lambda: "AnatomicalStructure", name="@type")
    subStructure: Union[List['AnatomicalStructure'], 'AnatomicalStructure', None] = None
    associatedPathophysiology: Union[List[str], str, None] = None
    diagram: Union[List['ImageObject'], 'ImageObject', None] = None
    relatedTherapy: Union[List['MedicalTherapy'], 'MedicalTherapy', None] = None
    relatedCondition: Union[List['MedicalCondition'], 'MedicalCondition', None] = None
    connectedTo: Union[List['AnatomicalStructure'], 'AnatomicalStructure', None] = None
    partOfSystem: Union[List['AnatomicalSystem'], 'AnatomicalSystem', None] = None
    bodyLocation: Union[List[str], str, None] = None