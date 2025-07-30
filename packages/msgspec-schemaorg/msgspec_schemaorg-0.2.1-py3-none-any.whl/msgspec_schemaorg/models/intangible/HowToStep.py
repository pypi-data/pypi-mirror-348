from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.ListItem import ListItem
from typing import Optional, Union, Dict, List, Any


class HowToStep(ListItem):
    """A step in the instructions for how to achieve a result. It is an ordered list with HowToDirection and/or HowToTip items."""
    type: str = field(default_factory=lambda: "HowToStep", name="@type")