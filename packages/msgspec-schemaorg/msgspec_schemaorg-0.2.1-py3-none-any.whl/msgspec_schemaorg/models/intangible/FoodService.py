from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Service import Service
from typing import Optional, Union, Dict, List, Any


class FoodService(Service):
    """A food service, like breakfast, lunch, or dinner."""
    type: str = field(default_factory=lambda: "FoodService", name="@type")