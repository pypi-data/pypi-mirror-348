from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.DoseSchedule import DoseSchedule
from typing import Optional, Union, Dict, List, Any


class RecommendedDoseSchedule(DoseSchedule):
    """A recommended dosing schedule for a drug or supplement as prescribed or recommended by an authority or by the drug/supplement's manufacturer. Capture the recommending authority in the recognizingAuthority property of MedicalEntity."""
    type: str = field(default_factory=lambda: "RecommendedDoseSchedule", name="@type")