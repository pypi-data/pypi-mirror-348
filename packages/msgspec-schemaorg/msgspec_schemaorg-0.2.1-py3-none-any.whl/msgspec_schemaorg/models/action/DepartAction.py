from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.MoveAction import MoveAction
from typing import Optional, Union, Dict, List, Any


class DepartAction(MoveAction):
    """The act of  departing from a place. An agent departs from a fromLocation for a destination, optionally with participants."""
    type: str = field(default_factory=lambda: "DepartAction", name="@type")