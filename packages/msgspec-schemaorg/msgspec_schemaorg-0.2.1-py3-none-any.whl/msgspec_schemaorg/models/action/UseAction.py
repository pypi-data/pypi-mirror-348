from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.ConsumeAction import ConsumeAction
from typing import Optional, Union, Dict, List, Any


class UseAction(ConsumeAction):
    """The act of applying an object to its intended purpose."""
    type: str = field(default_factory=lambda: "UseAction", name="@type")