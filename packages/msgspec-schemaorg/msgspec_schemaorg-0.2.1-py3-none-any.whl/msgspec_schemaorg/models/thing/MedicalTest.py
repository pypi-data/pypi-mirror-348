from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalEntity import MedicalEntity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.MedicalEnumeration import MedicalEnumeration
    from msgspec_schemaorg.models.product.Drug import Drug
    from msgspec_schemaorg.models.thing.MedicalCondition import MedicalCondition
    from msgspec_schemaorg.models.thing.MedicalDevice import MedicalDevice
    from msgspec_schemaorg.models.thing.MedicalSign import MedicalSign
from typing import Optional, Union, Dict, List, Any


class MedicalTest(MedicalEntity):
    """Any medical test, typically performed for diagnostic purposes."""
    type: str = field(default_factory=lambda: "MedicalTest", name="@type")
    usedToDiagnose: Union[List['MedicalCondition'], 'MedicalCondition', None] = None
    normalRange: Union[List[Union[str, 'MedicalEnumeration']], Union[str, 'MedicalEnumeration'], None] = None
    affectedBy: Union[List['Drug'], 'Drug', None] = None
    signDetected: Union[List['MedicalSign'], 'MedicalSign', None] = None
    usesDevice: Union[List['MedicalDevice'], 'MedicalDevice', None] = None