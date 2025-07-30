from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.MedicalOrganization import MedicalOrganization
from typing import Optional, Union, Dict, List, Any


class Pharmacy(MedicalOrganization):
    """A pharmacy or drugstore."""
    type: str = field(default_factory=lambda: "Pharmacy", name="@type")