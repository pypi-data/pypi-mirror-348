from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.AchieveAction import AchieveAction
from typing import Optional, Union, Dict, List, Any


class TieAction(AchieveAction):
    """The act of reaching a draw in a competitive activity."""
    type: str = field(default_factory=lambda: "TieAction", name="@type")