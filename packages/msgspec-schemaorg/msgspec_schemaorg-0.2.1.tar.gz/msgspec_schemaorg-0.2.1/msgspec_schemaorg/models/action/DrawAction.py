from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.CreateAction import CreateAction
from typing import Optional, Union, Dict, List, Any


class DrawAction(CreateAction):
    """The act of producing a visual/graphical representation of an object, typically with a pen/pencil and paper as instruments."""
    type: str = field(default_factory=lambda: "DrawAction", name="@type")