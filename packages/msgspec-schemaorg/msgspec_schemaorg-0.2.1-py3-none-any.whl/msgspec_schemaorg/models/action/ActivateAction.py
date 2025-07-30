from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.ControlAction import ControlAction
from typing import Optional, Union, Dict, List, Any


class ActivateAction(ControlAction):
    """The act of starting or activating a device or application (e.g. starting a timer or turning on a flashlight)."""
    type: str = field(default_factory=lambda: "ActivateAction", name="@type")