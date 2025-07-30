from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
from typing import Optional, Union, Dict, List, Any


class MeasurementTypeEnumeration(Enumeration):
    """Enumeration of common measurement types (or dimensions), for example "chest" for a person, "inseam" for pants, "gauge" for screws, or "wheel" for bicycles."""
    type: str = field(default_factory=lambda: "MeasurementTypeEnumeration", name="@type")