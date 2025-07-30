from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.HowToItem import HowToItem
from typing import Optional, Union, Dict, List, Any


class HowToTool(HowToItem):
    """A tool used (but not consumed) when performing instructions for how to achieve a result."""
    type: str = field(default_factory=lambda: "HowToTool", name="@type")