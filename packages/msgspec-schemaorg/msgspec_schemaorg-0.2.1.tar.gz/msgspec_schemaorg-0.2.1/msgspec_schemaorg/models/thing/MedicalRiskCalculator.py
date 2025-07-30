from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalRiskEstimator import MedicalRiskEstimator
from typing import Optional, Union, Dict, List, Any


class MedicalRiskCalculator(MedicalRiskEstimator):
    """A complex mathematical calculation requiring an online calculator, used to assess prognosis. Note: use the url property of Thing to record any URLs for online calculators."""
    type: str = field(default_factory=lambda: "MedicalRiskCalculator", name="@type")