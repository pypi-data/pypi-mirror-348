from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalCondition import MedicalCondition
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.InfectiousAgentClass import InfectiousAgentClass
from typing import Optional, Union, Dict, List, Any


class InfectiousDisease(MedicalCondition):
    """An infectious disease is a clinically evident human disease resulting from the presence of pathogenic microbial agents, like pathogenic viruses, pathogenic bacteria, fungi, protozoa, multicellular parasites, and prions. To be considered an infectious disease, such pathogens are known to be able to cause this disease."""
    type: str = field(default_factory=lambda: "InfectiousDisease", name="@type")
    infectiousAgentClass: Union[List['InfectiousAgentClass'], 'InfectiousAgentClass', None] = None
    infectiousAgent: Union[List[str], str, None] = None
    transmissionMethod: Union[List[str], str, None] = None