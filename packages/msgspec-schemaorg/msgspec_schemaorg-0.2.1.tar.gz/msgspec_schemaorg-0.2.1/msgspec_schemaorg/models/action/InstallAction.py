from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.ConsumeAction import ConsumeAction
from typing import Optional, Union, Dict, List, Any


class InstallAction(ConsumeAction):
    """The act of installing an application."""
    type: str = field(default_factory=lambda: "InstallAction", name="@type")