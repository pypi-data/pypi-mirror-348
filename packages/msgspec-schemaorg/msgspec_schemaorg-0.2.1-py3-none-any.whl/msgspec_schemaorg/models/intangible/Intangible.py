from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.Thing import Thing
from typing import Optional, Union, Dict, List, Any


class Intangible(Thing):
    """A utility class that serves as the umbrella for a number of 'intangible' things such as quantities, structured values, etc."""
    type: str = field(default_factory=lambda: "Intangible", name="@type")