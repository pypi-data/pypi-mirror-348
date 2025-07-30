from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.FindAction import FindAction
from typing import Optional, Union, Dict, List, Any


class DiscoverAction(FindAction):
    """The act of discovering/finding an object."""
    type: str = field(default_factory=lambda: "DiscoverAction", name="@type")