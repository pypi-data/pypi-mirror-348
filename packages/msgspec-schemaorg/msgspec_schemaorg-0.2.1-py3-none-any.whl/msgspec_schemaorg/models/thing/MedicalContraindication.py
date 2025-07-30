from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalEntity import MedicalEntity
from typing import Optional, Union, Dict, List, Any


class MedicalContraindication(MedicalEntity):
    """A condition or factor that serves as a reason to withhold a certain medical therapy. Contraindications can be absolute (there are no reasonable circumstances for undertaking a course of action) or relative (the patient is at higher risk of complications, but these risks may be outweighed by other considerations or mitigated by other measures)."""
    type: str = field(default_factory=lambda: "MedicalContraindication", name="@type")