from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.Vessel import Vessel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.thing.AnatomicalStructure import AnatomicalStructure
from typing import Optional, Union, Dict, List, Any


class Artery(Vessel):
    """A type of blood vessel that specifically carries blood away from the heart."""
    type: str = field(default_factory=lambda: "Artery", name="@type")
    arterialBranch: Union[List['AnatomicalStructure'], 'AnatomicalStructure', None] = None
    supplyTo: Union[List['AnatomicalStructure'], 'AnatomicalStructure', None] = None