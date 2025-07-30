from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.ReactAction import ReactAction
from typing import Optional, Union, Dict, List, Any


class LikeAction(ReactAction):
    """The act of expressing a positive sentiment about the object. An agent likes an object (a proposition, topic or theme) with participants."""
    type: str = field(default_factory=lambda: "LikeAction", name="@type")