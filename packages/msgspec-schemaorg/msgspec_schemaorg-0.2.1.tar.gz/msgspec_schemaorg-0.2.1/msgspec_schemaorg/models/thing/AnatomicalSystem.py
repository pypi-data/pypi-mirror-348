from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalEntity import MedicalEntity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.thing.AnatomicalStructure import AnatomicalStructure
    from msgspec_schemaorg.models.thing.AnatomicalSystem import AnatomicalSystem
    from msgspec_schemaorg.models.thing.MedicalCondition import MedicalCondition
    from msgspec_schemaorg.models.thing.MedicalTherapy import MedicalTherapy
from typing import Optional, Union, Dict, List, Any


class AnatomicalSystem(MedicalEntity):
    """An anatomical system is a group of anatomical structures that work together to perform a certain task. Anatomical systems, such as organ systems, are one organizing principle of anatomy, and can include circulatory, digestive, endocrine, integumentary, immune, lymphatic, muscular, nervous, reproductive, respiratory, skeletal, urinary, vestibular, and other systems."""
    type: str = field(default_factory=lambda: "AnatomicalSystem", name="@type")
    associatedPathophysiology: Union[List[str], str, None] = None
    relatedTherapy: Union[List['MedicalTherapy'], 'MedicalTherapy', None] = None
    relatedCondition: Union[List['MedicalCondition'], 'MedicalCondition', None] = None
    comprisedOf: Union[List[Union['AnatomicalStructure', 'AnatomicalSystem']], Union['AnatomicalStructure', 'AnatomicalSystem'], None] = None
    relatedStructure: Union[List['AnatomicalStructure'], 'AnatomicalStructure', None] = None