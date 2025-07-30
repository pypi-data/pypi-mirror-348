from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class Quotation(CreativeWork):
    """A quotation. Often but not necessarily from some written work, attributable to a real world author and - if associated with a fictional character - to any fictional Person. Use [[isBasedOn]] to link to source/origin. The [[recordedIn]] property can be used to reference a Quotation from an [[Event]]."""
    type: str = field(default_factory=lambda: "Quotation", name="@type")
    spokenByCharacter: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None