from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.CommunicateAction import CommunicateAction
from typing import Optional, Union, Dict, List, Any


class ShareAction(CommunicateAction):
    """The act of distributing content to people for their amusement or edification."""
    type: str = field(default_factory=lambda: "ShareAction", name="@type")