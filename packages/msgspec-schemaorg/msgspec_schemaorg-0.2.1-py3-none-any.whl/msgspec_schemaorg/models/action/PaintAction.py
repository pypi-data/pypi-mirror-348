from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.CreateAction import CreateAction
from typing import Optional, Union, Dict, List, Any


class PaintAction(CreateAction):
    """The act of producing a painting, typically with paint and canvas as instruments."""
    type: str = field(default_factory=lambda: "PaintAction", name="@type")