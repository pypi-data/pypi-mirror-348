from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.AlignmentObject import AlignmentObject
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
from typing import Optional, Union, Dict, List, Any


class LearningResource(CreativeWork):
    """The LearningResource type can be used to indicate [[CreativeWork]]s (whether physical or digital) that have a particular and explicit orientation towards learning, education, skill acquisition, and other educational purposes.

[[LearningResource]] is expected to be used as an addition to a primary type such as [[Book]], [[VideoObject]], [[Product]] etc.

[[EducationEvent]] serves a similar purpose for event-like things (e.g. a [[Trip]]). A [[LearningResource]] may be created as a result of an [[EducationEvent]], for example by recording one."""
    type: str = field(default_factory=lambda: "LearningResource", name="@type")
    educationalAlignment: Union[List['AlignmentObject'], 'AlignmentObject', None] = None
    educationalUse: Union[List[Union[str, 'DefinedTerm']], Union[str, 'DefinedTerm'], None] = None
    assesses: Union[List[Union[str, 'DefinedTerm']], Union[str, 'DefinedTerm'], None] = None
    teaches: Union[List[Union[str, 'DefinedTerm']], Union[str, 'DefinedTerm'], None] = None
    educationalLevel: Union[List[Union['URL', str, 'DefinedTerm']], Union['URL', str, 'DefinedTerm'], None] = None
    learningResourceType: Union[List[Union[str, 'DefinedTerm']], Union[str, 'DefinedTerm'], None] = None
    competencyRequired: Union[List[Union['URL', str, 'DefinedTerm']], Union['URL', str, 'DefinedTerm'], None] = None