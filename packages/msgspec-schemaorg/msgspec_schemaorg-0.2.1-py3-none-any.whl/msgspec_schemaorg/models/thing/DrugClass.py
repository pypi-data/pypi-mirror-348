from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalEntity import MedicalEntity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.product.Drug import Drug
from typing import Optional, Union, Dict, List, Any


class DrugClass(MedicalEntity):
    """A class of medical drugs, e.g., statins. Classes can represent general pharmacological class, common mechanisms of action, common physiological effects, etc."""
    type: str = field(default_factory=lambda: "DrugClass", name="@type")
    drug: Union[List['Drug'], 'Drug', None] = None