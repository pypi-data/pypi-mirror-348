from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.Action import Action
from typing import Optional, Union, Dict, List, Any


class AchieveAction(Action):
    """The act of accomplishing something via previous efforts. It is an instantaneous action rather than an ongoing process."""
    type: str = field(default_factory=lambda: "AchieveAction", name="@type")