from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.action.AssessAction import AssessAction
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Review import Review
from typing import Optional, Union, Dict, List, Any


class ReviewAction(AssessAction):
    """The act of producing a balanced opinion about the object for an audience. An agent reviews an object with participants resulting in a review."""
    type: str = field(default_factory=lambda: "ReviewAction", name="@type")
    resultReview: Union[List['Review'], 'Review', None] = None