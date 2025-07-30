from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.LodgingBusiness import LodgingBusiness
from typing import Optional, Union, Dict, List, Any


class VacationRental(LodgingBusiness):
    """A kind of lodging business that focuses on renting single properties for limited time."""
    type: str = field(default_factory=lambda: "VacationRental", name="@type")