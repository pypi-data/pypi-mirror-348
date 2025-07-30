from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.AchieveAction import AchieveAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class LoseAction(AchieveAction):
    """The act of being defeated in a competitive activity."""
    type: str = field(default_factory=lambda: "LoseAction", name="@type")
    winner: Union[List['Person'], 'Person', None] = None