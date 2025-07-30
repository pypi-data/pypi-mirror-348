from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.ControlAction import ControlAction
from typing import Optional, Union, Dict, List, Any


class ResumeAction(ControlAction):
    """The act of resuming a device or application which was formerly paused (e.g. resume music playback or resume a timer)."""
    type: str = field(default_factory=lambda: "ResumeAction", name="@type")