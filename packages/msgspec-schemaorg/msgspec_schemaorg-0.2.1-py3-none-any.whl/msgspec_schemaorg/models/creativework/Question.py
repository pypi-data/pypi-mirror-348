from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.Comment import Comment
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Answer import Answer
    from msgspec_schemaorg.models.creativework.Comment import Comment
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.intangible.ItemList import ItemList
from typing import Optional, Union, Dict, List, Any


class Question(Comment):
    """A specific question - e.g. from a user seeking answers online, or collected in a Frequently Asked Questions (FAQ) document."""
    type: str = field(default_factory=lambda: "Question", name="@type")
    parentItem: Union[List[Union['Comment', 'CreativeWork']], Union['Comment', 'CreativeWork'], None] = None
    answerCount: Union[List[int], int, None] = None
    suggestedAnswer: Union[List[Union['ItemList', 'Answer']], Union['ItemList', 'Answer'], None] = None
    eduQuestionType: Union[List[str], str, None] = None
    acceptedAnswer: Union[List[Union['ItemList', 'Answer']], Union['ItemList', 'Answer'], None] = None