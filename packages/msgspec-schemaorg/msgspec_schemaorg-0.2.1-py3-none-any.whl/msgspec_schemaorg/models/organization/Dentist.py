from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.MedicalOrganization import MedicalOrganization
from typing import Optional, Union, Dict, List, Any


class Dentist(MedicalOrganization):
    """A dentist."""
    type: str = field(default_factory=lambda: "Dentist", name="@type")