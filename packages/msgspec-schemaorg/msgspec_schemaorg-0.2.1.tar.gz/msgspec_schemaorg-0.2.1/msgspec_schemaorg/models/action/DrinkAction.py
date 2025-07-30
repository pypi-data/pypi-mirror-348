from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.ConsumeAction import ConsumeAction
from typing import Optional, Union, Dict, List, Any


class DrinkAction(ConsumeAction):
    """The act of swallowing liquids."""
    type: str = field(default_factory=lambda: "DrinkAction", name="@type")