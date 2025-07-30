from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.AssessAction import AssessAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.thing.Thing import Thing
from typing import Optional, Union, Dict, List, Any


class ChooseAction(AssessAction):
    """The act of expressing a preference from a set of options or a large or unbounded set of choices/options."""
    type: str = field(default_factory=lambda: "ChooseAction", name="@type")
    option: Union[List[Union[str, 'Thing']], Union[str, 'Thing'], None] = None
    actionOption: Union[List[Union[str, 'Thing']], Union[str, 'Thing'], None] = None