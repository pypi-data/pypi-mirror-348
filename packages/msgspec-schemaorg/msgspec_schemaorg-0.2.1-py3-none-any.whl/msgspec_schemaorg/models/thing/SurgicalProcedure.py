from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalProcedure import MedicalProcedure
from typing import Optional, Union, Dict, List, Any


class SurgicalProcedure(MedicalProcedure):
    """A medical procedure involving an incision with instruments; performed for diagnose, or therapeutic purposes."""
    type: str = field(default_factory=lambda: "SurgicalProcedure", name="@type")