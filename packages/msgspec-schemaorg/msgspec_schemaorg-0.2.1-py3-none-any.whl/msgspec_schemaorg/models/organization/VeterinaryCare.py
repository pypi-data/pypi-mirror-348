from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.MedicalOrganization import MedicalOrganization
from typing import Optional, Union, Dict, List, Any


class VeterinaryCare(MedicalOrganization):
    """A vet's office."""
    type: str = field(default_factory=lambda: "VeterinaryCare", name="@type")