from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.LocalBusiness import LocalBusiness
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.ArchiveComponent import ArchiveComponent
from typing import Optional, Union, Dict, List, Any


class ArchiveOrganization(LocalBusiness):
    """{'@language': 'en', '@value': 'An organization with archival holdings. An organization which keeps and preserves archival material and typically makes it accessible to the public.'}"""
    type: str = field(default_factory=lambda: "ArchiveOrganization", name="@type")
    archiveHeld: Union[List['ArchiveComponent'], 'ArchiveComponent', None] = None