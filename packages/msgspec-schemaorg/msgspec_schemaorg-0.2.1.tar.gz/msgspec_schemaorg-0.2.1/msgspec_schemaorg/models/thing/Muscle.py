from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.AnatomicalStructure import AnatomicalStructure
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.thing.AnatomicalStructure import AnatomicalStructure
    from msgspec_schemaorg.models.thing.Muscle import Muscle
    from msgspec_schemaorg.models.thing.Nerve import Nerve
    from msgspec_schemaorg.models.thing.Vessel import Vessel
from typing import Optional, Union, Dict, List, Any


class Muscle(AnatomicalStructure):
    """A muscle is an anatomical structure consisting of a contractile form of tissue that animals use to effect movement."""
    type: str = field(default_factory=lambda: "Muscle", name="@type")
    nerve: Union[List['Nerve'], 'Nerve', None] = None
    antagonist: Union[List['Muscle'], 'Muscle', None] = None
    bloodSupply: Union[List['Vessel'], 'Vessel', None] = None
    muscleAction: Union[List[str], str, None] = None
    insertion: Union[List['AnatomicalStructure'], 'AnatomicalStructure', None] = None