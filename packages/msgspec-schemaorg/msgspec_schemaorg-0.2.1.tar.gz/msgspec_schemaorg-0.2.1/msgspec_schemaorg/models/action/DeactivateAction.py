from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.ControlAction import ControlAction
from typing import Optional, Union, Dict, List, Any


class DeactivateAction(ControlAction):
    """The act of stopping or deactivating a device or application (e.g. stopping a timer or turning off a flashlight)."""
    type: str = field(default_factory=lambda: "DeactivateAction", name="@type")