from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalRiskEstimator import MedicalRiskEstimator
from typing import Optional, Union, Dict, List, Any


class MedicalRiskScore(MedicalRiskEstimator):
    """A simple system that adds up the number of risk factors to yield a score that is associated with prognosis, e.g. CHAD score, TIMI risk score."""
    type: str = field(default_factory=lambda: "MedicalRiskScore", name="@type")
    algorithm: Union[List[str], str, None] = None