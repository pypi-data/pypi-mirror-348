from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.RadioChannel import RadioChannel
from typing import Optional, Union, Dict, List, Any


class FMRadioChannel(RadioChannel):
    """A radio channel that uses FM."""
    type: str = field(default_factory=lambda: "FMRadioChannel", name="@type")