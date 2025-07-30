from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.AssessAction import AssessAction
from typing import Optional, Union, Dict, List, Any


class IgnoreAction(AssessAction):
    """The act of intentionally disregarding the object. An agent ignores an object."""
    type: str = field(default_factory=lambda: "IgnoreAction", name="@type")