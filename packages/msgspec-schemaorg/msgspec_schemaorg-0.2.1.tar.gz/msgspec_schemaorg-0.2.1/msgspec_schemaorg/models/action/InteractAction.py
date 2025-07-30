from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.Action import Action
from typing import Optional, Union, Dict, List, Any


class InteractAction(Action):
    """The act of interacting with another person or organization."""
    type: str = field(default_factory=lambda: "InteractAction", name="@type")