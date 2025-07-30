from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.AnatomicalStructure import AnatomicalStructure
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.thing.AnatomicalStructure import AnatomicalStructure
    from msgspec_schemaorg.models.thing.BrainStructure import BrainStructure
    from msgspec_schemaorg.models.thing.Muscle import Muscle
    from msgspec_schemaorg.models.thing.SuperficialAnatomy import SuperficialAnatomy
from typing import Optional, Union, Dict, List, Any


class Nerve(AnatomicalStructure):
    """A common pathway for the electrochemical nerve impulses that are transmitted along each of the axons."""
    type: str = field(default_factory=lambda: "Nerve", name="@type")
    nerveMotor: Union[List['Muscle'], 'Muscle', None] = None
    sourcedFrom: Union[List['BrainStructure'], 'BrainStructure', None] = None
    sensoryUnit: Union[List[Union['AnatomicalStructure', 'SuperficialAnatomy']], Union['AnatomicalStructure', 'SuperficialAnatomy'], None] = None
    branch: Union[List['AnatomicalStructure'], 'AnatomicalStructure', None] = None