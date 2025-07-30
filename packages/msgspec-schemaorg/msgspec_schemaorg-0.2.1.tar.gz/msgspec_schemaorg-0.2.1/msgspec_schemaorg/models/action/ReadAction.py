from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.ConsumeAction import ConsumeAction
from typing import Optional, Union, Dict, List, Any


class ReadAction(ConsumeAction):
    """The act of consuming written content."""
    type: str = field(default_factory=lambda: "ReadAction", name="@type")