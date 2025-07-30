from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.ControlAction import ControlAction
from typing import Optional, Union, Dict, List, Any


class SuspendAction(ControlAction):
    """The act of momentarily pausing a device or application (e.g. pause music playback or pause a timer)."""
    type: str = field(default_factory=lambda: "SuspendAction", name="@type")