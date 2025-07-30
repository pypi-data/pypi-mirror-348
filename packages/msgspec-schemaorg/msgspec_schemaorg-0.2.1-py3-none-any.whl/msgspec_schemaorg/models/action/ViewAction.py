from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.ConsumeAction import ConsumeAction
from typing import Optional, Union, Dict, List, Any


class ViewAction(ConsumeAction):
    """The act of consuming static visual content."""
    type: str = field(default_factory=lambda: "ViewAction", name="@type")