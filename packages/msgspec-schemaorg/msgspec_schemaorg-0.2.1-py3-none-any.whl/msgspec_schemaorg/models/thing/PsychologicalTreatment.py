from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.TherapeuticProcedure import TherapeuticProcedure
from typing import Optional, Union, Dict, List, Any


class PsychologicalTreatment(TherapeuticProcedure):
    """A process of care relying upon counseling, dialogue and communication  aimed at improving a mental health condition without use of drugs."""
    type: str = field(default_factory=lambda: "PsychologicalTreatment", name="@type")