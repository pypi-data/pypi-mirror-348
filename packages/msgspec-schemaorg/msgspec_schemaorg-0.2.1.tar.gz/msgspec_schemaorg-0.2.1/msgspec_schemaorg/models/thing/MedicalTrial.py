from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalStudy import MedicalStudy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.MedicalTrialDesign import MedicalTrialDesign
from typing import Optional, Union, Dict, List, Any


class MedicalTrial(MedicalStudy):
    """A medical trial is a type of medical study that uses a scientific process to compare the safety and efficacy of medical therapies or medical procedures. In general, medical trials are controlled and subjects are allocated at random to the different treatment and/or control groups."""
    type: str = field(default_factory=lambda: "MedicalTrial", name="@type")
    trialDesign: Union[List['MedicalTrialDesign'], 'MedicalTrialDesign', None] = None