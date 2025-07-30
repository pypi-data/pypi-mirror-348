from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.FindAction import FindAction
from typing import Optional, Union, Dict, List, Any


class CheckAction(FindAction):
    """An agent inspects, determines, investigates, inquires, or examines an object's accuracy, quality, condition, or state."""
    type: str = field(default_factory=lambda: "CheckAction", name="@type")