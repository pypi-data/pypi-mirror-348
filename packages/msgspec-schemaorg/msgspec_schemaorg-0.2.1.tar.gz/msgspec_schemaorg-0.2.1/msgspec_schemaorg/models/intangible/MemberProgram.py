from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.MemberProgramTier import MemberProgramTier
    from msgspec_schemaorg.models.organization.Organization import Organization
from typing import Optional, Union, Dict, List, Any


class MemberProgram(Intangible):
    """A MemberProgram defines a loyalty (or membership) program that provides its members with certain benefits, for example better pricing, free shipping or returns, or the ability to earn loyalty points. Member programs may have multiple tiers, for example silver and gold members, each with different benefits."""
    type: str = field(default_factory=lambda: "MemberProgram", name="@type")
    hasTiers: Union[List['MemberProgramTier'], 'MemberProgramTier', None] = None
    hostingOrganization: Union[List['Organization'], 'Organization', None] = None