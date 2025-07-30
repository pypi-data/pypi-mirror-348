from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.MemberProgram import MemberProgram
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class ProgramMembership(Intangible):
    """Used to describe membership in a loyalty programs (e.g. "StarAliance"), traveler clubs (e.g. "AAA"), purchase clubs ("Safeway Club"), etc."""
    type: str = field(default_factory=lambda: "ProgramMembership", name="@type")
    member: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    members: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    membershipNumber: Union[List[str], str, None] = None
    program: Union[List['MemberProgram'], 'MemberProgram', None] = None
    membershipPointsEarned: Union[List[Union[int | float, 'QuantitativeValue']], Union[int | float, 'QuantitativeValue'], None] = None
    hostingOrganization: Union[List['Organization'], 'Organization', None] = None
    programName: Union[List[str], str, None] = None