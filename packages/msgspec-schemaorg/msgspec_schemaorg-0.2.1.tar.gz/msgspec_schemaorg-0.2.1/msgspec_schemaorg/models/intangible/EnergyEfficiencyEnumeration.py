from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class EnergyEfficiencyEnumeration(Enumeration):
    """Enumerates energy efficiency levels (also known as "classes" or "ratings") and certifications that are part of several international energy efficiency standards."""
    type: str = field(default_factory=lambda: "EnergyEfficiencyEnumeration", name="@type")