from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.UseAction import UseAction
from typing import Optional, Union, Dict, List, Any


class WearAction(UseAction):
    """The act of dressing oneself in clothing."""
    type: str = field(default_factory=lambda: "WearAction", name="@type")