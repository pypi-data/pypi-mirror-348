from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.Action import Action
from typing import Optional, Union, Dict, List, Any


class ControlAction(Action):
    """An agent controls a device or application."""
    type: str = field(default_factory=lambda: "ControlAction", name="@type")