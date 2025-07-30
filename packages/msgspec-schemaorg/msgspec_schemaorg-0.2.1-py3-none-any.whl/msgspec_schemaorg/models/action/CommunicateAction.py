from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.InteractAction import InteractAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Audience import Audience
    from msgspec_schemaorg.models.intangible.ContactPoint import ContactPoint
    from msgspec_schemaorg.models.intangible.Language import Language
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.thing.Thing import Thing
from typing import Optional, Union, Dict, List, Any


class CommunicateAction(InteractAction):
    """The act of conveying information to another person via a communication medium (instrument) such as speech, email, or telephone conversation."""
    type: str = field(default_factory=lambda: "CommunicateAction", name="@type")
    about: Union[List['Thing'], 'Thing', None] = None
    language: Union[List['Language'], 'Language', None] = None
    inLanguage: Union[List[Union[str, 'Language']], Union[str, 'Language'], None] = None
    recipient: Union[List[Union['Organization', 'Audience', 'ContactPoint', 'Person']], Union['Organization', 'Audience', 'ContactPoint', 'Person'], None] = None