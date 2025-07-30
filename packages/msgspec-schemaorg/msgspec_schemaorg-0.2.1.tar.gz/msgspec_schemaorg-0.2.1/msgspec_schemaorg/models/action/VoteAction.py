from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.ChooseAction import ChooseAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class VoteAction(ChooseAction):
    """The act of expressing a preference from a fixed/finite/structured set of choices/options."""
    type: str = field(default_factory=lambda: "VoteAction", name="@type")
    candidate: Union[List['Person'], 'Person', None] = None