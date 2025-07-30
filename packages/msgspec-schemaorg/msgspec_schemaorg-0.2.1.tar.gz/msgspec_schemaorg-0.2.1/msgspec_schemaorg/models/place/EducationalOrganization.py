from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.place.CivicStructure import CivicStructure
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class EducationalOrganization(CivicStructure):
    """An educational organization."""
    type: str = field(default_factory=lambda: "EducationalOrganization", name="@type")
    alumni: Union[List['Person'], 'Person', None] = None