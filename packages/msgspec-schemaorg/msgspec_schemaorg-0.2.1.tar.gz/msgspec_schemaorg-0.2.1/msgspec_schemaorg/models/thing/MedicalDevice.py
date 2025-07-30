from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalEntity import MedicalEntity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.thing.MedicalContraindication import MedicalContraindication
    from msgspec_schemaorg.models.thing.MedicalEntity import MedicalEntity
from typing import Optional, Union, Dict, List, Any


class MedicalDevice(MedicalEntity):
    """Any object used in a medical capacity, such as to diagnose or treat a patient."""
    type: str = field(default_factory=lambda: "MedicalDevice", name="@type")
    preOp: Union[List[str], str, None] = None
    postOp: Union[List[str], str, None] = None
    contraindication: Union[List[Union[str, 'MedicalContraindication']], Union[str, 'MedicalContraindication'], None] = None
    seriousAdverseOutcome: Union[List['MedicalEntity'], 'MedicalEntity', None] = None
    procedure: Union[List[str], str, None] = None
    adverseOutcome: Union[List['MedicalEntity'], 'MedicalEntity', None] = None