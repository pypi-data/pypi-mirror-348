from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Audience import Audience
    from msgspec_schemaorg.models.intangible.ContactPoint import ContactPoint
    from msgspec_schemaorg.enums.intangible.DigitalDocumentPermissionType import DigitalDocumentPermissionType
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class DigitalDocumentPermission(Intangible):
    """A permission for a particular person or group to access a particular file."""
    type: str = field(default_factory=lambda: "DigitalDocumentPermission", name="@type")
    permissionType: Union[List['DigitalDocumentPermissionType'], 'DigitalDocumentPermissionType', None] = None
    grantee: Union[List[Union['Audience', 'Organization', 'ContactPoint', 'Person']], Union['Audience', 'Organization', 'ContactPoint', 'Person'], None] = None