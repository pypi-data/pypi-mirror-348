from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.MoveAction import MoveAction
from typing import Optional, Union, Dict, List, Any


class ArriveAction(MoveAction):
    """The act of arriving at a place. An agent arrives at a destination from a fromLocation, optionally with participants."""
    type: str = field(default_factory=lambda: "ArriveAction", name="@type")