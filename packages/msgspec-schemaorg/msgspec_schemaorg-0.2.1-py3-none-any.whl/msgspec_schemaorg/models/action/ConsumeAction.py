from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.Action import Action
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.ActionAccessSpecification import ActionAccessSpecification
    from msgspec_schemaorg.models.intangible.Offer import Offer
from typing import Optional, Union, Dict, List, Any


class ConsumeAction(Action):
    """The act of ingesting information/resources/food."""
    type: str = field(default_factory=lambda: "ConsumeAction", name="@type")
    actionAccessibilityRequirement: Union[List['ActionAccessSpecification'], 'ActionAccessSpecification', None] = None
    expectsAcceptanceOf: Union[List['Offer'], 'Offer', None] = None