from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.ReactAction import ReactAction
from typing import Optional, Union, Dict, List, Any


class WantAction(ReactAction):
    """The act of expressing a desire about the object. An agent wants an object."""
    type: str = field(default_factory=lambda: "WantAction", name="@type")