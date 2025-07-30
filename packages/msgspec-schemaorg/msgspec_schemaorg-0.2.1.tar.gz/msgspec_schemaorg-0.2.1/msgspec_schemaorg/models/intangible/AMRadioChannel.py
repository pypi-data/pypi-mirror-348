from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.RadioChannel import RadioChannel
from typing import Optional, Union, Dict, List, Any


class AMRadioChannel(RadioChannel):
    """A radio channel that uses AM."""
    type: str = field(default_factory=lambda: "AMRadioChannel", name="@type")