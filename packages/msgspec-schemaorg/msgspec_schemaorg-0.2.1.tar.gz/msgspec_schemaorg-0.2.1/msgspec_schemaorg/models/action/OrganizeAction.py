from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.Action import Action
from typing import Optional, Union, Dict, List, Any


class OrganizeAction(Action):
    """The act of manipulating/administering/supervising/controlling one or more objects."""
    type: str = field(default_factory=lambda: "OrganizeAction", name="@type")