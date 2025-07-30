from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.QualitativeValue import QualitativeValue
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
from typing import Optional, Union, Dict, List, Any


class BroadcastFrequencySpecification(Intangible):
    """The frequency in MHz and the modulation used for a particular BroadcastService."""
    type: str = field(default_factory=lambda: "BroadcastFrequencySpecification", name="@type")
    broadcastFrequencyValue: Union[List[Union[int | float, 'QuantitativeValue']], Union[int | float, 'QuantitativeValue'], None] = None
    broadcastSignalModulation: Union[List[Union[str, 'QualitativeValue']], Union[str, 'QualitativeValue'], None] = None
    broadcastSubChannel: Union[List[str], str, None] = None