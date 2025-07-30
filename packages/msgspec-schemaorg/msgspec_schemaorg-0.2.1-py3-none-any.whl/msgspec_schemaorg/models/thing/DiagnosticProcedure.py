from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalProcedure import MedicalProcedure
from typing import Optional, Union, Dict, List, Any


class DiagnosticProcedure(MedicalProcedure):
    """A medical procedure intended primarily for diagnostic, as opposed to therapeutic, purposes."""
    type: str = field(default_factory=lambda: "DiagnosticProcedure", name="@type")