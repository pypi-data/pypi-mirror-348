from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.ConsumeAction import ConsumeAction
from typing import Optional, Union, Dict, List, Any


class EatAction(ConsumeAction):
    """The act of swallowing solid objects."""
    type: str = field(default_factory=lambda: "EatAction", name="@type")