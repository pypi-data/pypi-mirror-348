from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Service import Service
from typing import Optional, Union, Dict, List, Any


class Taxi(Service):
    """A taxi."""
    type: str = field(default_factory=lambda: "Taxi", name="@type")