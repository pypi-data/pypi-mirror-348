from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.Action import Action
from typing import Optional, Union, Dict, List, Any


class AssessAction(Action):
    """The act of forming one's opinion, reaction or sentiment."""
    type: str = field(default_factory=lambda: "AssessAction", name="@type")