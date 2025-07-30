from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.PerformingGroup import PerformingGroup
from typing import Optional, Union, Dict, List, Any


class TheaterGroup(PerformingGroup):
    """A theater group or company, for example, the Royal Shakespeare Company or Druid Theatre."""
    type: str = field(default_factory=lambda: "TheaterGroup", name="@type")