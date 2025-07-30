from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.ReactAction import ReactAction
from typing import Optional, Union, Dict, List, Any


class DislikeAction(ReactAction):
    """The act of expressing a negative sentiment about the object. An agent dislikes an object (a proposition, topic or theme) with participants."""
    type: str = field(default_factory=lambda: "DislikeAction", name="@type")