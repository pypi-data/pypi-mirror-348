from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.MedicalBusiness import MedicalBusiness
from typing import Optional, Union, Dict, List, Any


class Optician(MedicalBusiness):
    """A store that sells reading glasses and similar devices for improving vision."""
    type: str = field(default_factory=lambda: "Optician", name="@type")