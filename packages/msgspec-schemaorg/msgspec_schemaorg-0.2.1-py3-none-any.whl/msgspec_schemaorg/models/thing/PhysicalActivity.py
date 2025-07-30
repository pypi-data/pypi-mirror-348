from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.LifestyleModification import LifestyleModification
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.CategoryCode import CategoryCode
    from msgspec_schemaorg.enums.intangible.PhysicalActivityCategory import PhysicalActivityCategory
    from msgspec_schemaorg.models.thing.AnatomicalStructure import AnatomicalStructure
    from msgspec_schemaorg.models.thing.AnatomicalSystem import AnatomicalSystem
    from msgspec_schemaorg.models.thing.SuperficialAnatomy import SuperficialAnatomy
    from msgspec_schemaorg.models.thing.Thing import Thing
from typing import Optional, Union, Dict, List, Any


class PhysicalActivity(LifestyleModification):
    """Any bodily activity that enhances or maintains physical fitness and overall health and wellness. Includes activity that is part of daily living and routine, structured exercise, and exercise prescribed as part of a medical treatment or recovery plan."""
    type: str = field(default_factory=lambda: "PhysicalActivity", name="@type")
    category: Union[List[Union['URL', str, 'Thing', 'PhysicalActivityCategory', 'CategoryCode']], Union['URL', str, 'Thing', 'PhysicalActivityCategory', 'CategoryCode'], None] = None
    associatedAnatomy: Union[List[Union['AnatomicalStructure', 'SuperficialAnatomy', 'AnatomicalSystem']], Union['AnatomicalStructure', 'SuperficialAnatomy', 'AnatomicalSystem'], None] = None
    epidemiology: Union[List[str], str, None] = None
    pathophysiology: Union[List[str], str, None] = None