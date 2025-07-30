from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.Action import Action
from typing import Optional, Union, Dict, List, Any


class SolveMathAction(Action):
    """The action that takes in a math expression and directs users to a page potentially capable of solving/simplifying that expression."""
    type: str = field(default_factory=lambda: "SolveMathAction", name="@type")
    eduQuestionType: Union[List[str], str, None] = None