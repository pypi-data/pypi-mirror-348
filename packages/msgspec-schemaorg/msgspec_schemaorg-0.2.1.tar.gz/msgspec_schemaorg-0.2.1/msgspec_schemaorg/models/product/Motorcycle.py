from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.product.Vehicle import Vehicle
from typing import Optional, Union, Dict, List, Any


class Motorcycle(Vehicle):
    """A motorcycle or motorbike is a single-track, two-wheeled motor vehicle."""
    type: str = field(default_factory=lambda: "Motorcycle", name="@type")