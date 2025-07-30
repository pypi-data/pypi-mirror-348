from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.product.Vehicle import Vehicle
from typing import Optional, Union, Dict, List, Any


class MotorizedBicycle(Vehicle):
    """A motorized bicycle is a bicycle with an attached motor used to power the vehicle, or to assist with pedaling."""
    type: str = field(default_factory=lambda: "MotorizedBicycle", name="@type")