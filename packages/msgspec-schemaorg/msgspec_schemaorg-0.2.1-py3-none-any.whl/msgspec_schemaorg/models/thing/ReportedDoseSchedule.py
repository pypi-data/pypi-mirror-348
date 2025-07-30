from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.DoseSchedule import DoseSchedule
from typing import Optional, Union, Dict, List, Any


class ReportedDoseSchedule(DoseSchedule):
    """A patient-reported or observed dosing schedule for a drug or supplement."""
    type: str = field(default_factory=lambda: "ReportedDoseSchedule", name="@type")