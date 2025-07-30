from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class Diet(CreativeWork):
    """A strategy of regulating the intake of food to achieve or maintain a specific health-related goal."""
    type: str = field(default_factory=lambda: "Diet", name="@type")
    expertConsiderations: Union[List[str], str, None] = None
    dietFeatures: Union[List[str], str, None] = None
    physiologicalBenefits: Union[List[str], str, None] = None
    endorsers: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    risks: Union[List[str], str, None] = None