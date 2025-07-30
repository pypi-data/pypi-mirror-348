from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.BedType import BedType
from typing import Optional, Union, Dict, List, Any


class BedDetails(Intangible):
    """An entity holding detailed information about the available bed types, e.g. the quantity of twin beds for a hotel room. For the single case of just one bed of a certain type, you can use bed directly with a text. See also [[BedType]] (under development)."""
    type: str = field(default_factory=lambda: "BedDetails", name="@type")
    typeOfBed: Union[List[Union[str, 'BedType']], Union[str, 'BedType'], None] = None
    numberOfBeds: Union[List[int | float], int | float, None] = None