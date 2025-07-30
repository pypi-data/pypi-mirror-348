from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalTest import MedicalTest
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.MedicalImagingTechnique import MedicalImagingTechnique
from typing import Optional, Union, Dict, List, Any


class ImagingTest(MedicalTest):
    """Any medical imaging modality typically used for diagnostic purposes."""
    type: str = field(default_factory=lambda: "ImagingTest", name="@type")
    imagingTechnique: Union[List['MedicalImagingTechnique'], 'MedicalImagingTechnique', None] = None