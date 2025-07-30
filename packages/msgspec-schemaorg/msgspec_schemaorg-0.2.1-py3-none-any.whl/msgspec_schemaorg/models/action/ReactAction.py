from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.AssessAction import AssessAction
from typing import Optional, Union, Dict, List, Any


class ReactAction(AssessAction):
    """The act of responding instinctively and emotionally to an object, expressing a sentiment."""
    type: str = field(default_factory=lambda: "ReactAction", name="@type")