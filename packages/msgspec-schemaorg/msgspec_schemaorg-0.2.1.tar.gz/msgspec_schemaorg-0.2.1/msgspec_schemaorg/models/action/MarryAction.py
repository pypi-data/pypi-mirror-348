from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.InteractAction import InteractAction
from typing import Optional, Union, Dict, List, Any


class MarryAction(InteractAction):
    """The act of marrying a person."""
    type: str = field(default_factory=lambda: "MarryAction", name="@type")