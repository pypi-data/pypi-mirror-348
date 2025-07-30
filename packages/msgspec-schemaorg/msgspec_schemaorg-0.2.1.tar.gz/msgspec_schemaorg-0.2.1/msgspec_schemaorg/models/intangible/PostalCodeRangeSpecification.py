from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from typing import Optional, Union, Dict, List, Any


class PostalCodeRangeSpecification(StructuredValue):
    """Indicates a range of postal codes, usually defined as the set of valid codes between [[postalCodeBegin]] and [[postalCodeEnd]], inclusively."""
    type: str = field(default_factory=lambda: "PostalCodeRangeSpecification", name="@type")
    postalCodeEnd: Union[List[str], str, None] = None
    postalCodeBegin: Union[List[str], str, None] = None