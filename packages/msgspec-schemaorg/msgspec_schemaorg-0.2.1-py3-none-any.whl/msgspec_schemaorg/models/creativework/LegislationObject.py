from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.Legislation import Legislation
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.LegalValueLevel import LegalValueLevel
from typing import Optional, Union, Dict, List, Any


class LegislationObject(Legislation):
    """A specific object or file containing a Legislation. Note that the same Legislation can be published in multiple files. For example, a digitally signed PDF, a plain PDF and an HTML version."""
    type: str = field(default_factory=lambda: "LegislationObject", name="@type")
    legislationLegalValue: Union[List['LegalValueLevel'], 'LegalValueLevel', None] = None