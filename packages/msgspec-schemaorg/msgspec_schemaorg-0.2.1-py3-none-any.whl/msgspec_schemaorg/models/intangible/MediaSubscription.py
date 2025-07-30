from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Offer import Offer
    from msgspec_schemaorg.models.organization.Organization import Organization
from typing import Optional, Union, Dict, List, Any


class MediaSubscription(Intangible):
    """A subscription which allows a user to access media including audio, video, books, etc."""
    type: str = field(default_factory=lambda: "MediaSubscription", name="@type")
    authenticator: Union[List['Organization'], 'Organization', None] = None
    expectsAcceptanceOf: Union[List['Offer'], 'Offer', None] = None