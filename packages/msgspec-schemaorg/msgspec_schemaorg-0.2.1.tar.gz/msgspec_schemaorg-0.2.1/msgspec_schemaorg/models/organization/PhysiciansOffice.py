from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.Physician import Physician
from typing import Optional, Union, Dict, List, Any


class PhysiciansOffice(Physician):
    """A doctor's office or clinic."""
    type: str = field(default_factory=lambda: "PhysiciansOffice", name="@type")