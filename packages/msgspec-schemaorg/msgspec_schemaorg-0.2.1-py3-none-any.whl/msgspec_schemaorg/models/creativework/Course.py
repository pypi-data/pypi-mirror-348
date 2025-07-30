from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.LearningResource import LearningResource
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Course import Course
    from msgspec_schemaorg.models.creativework.EducationalOccupationalCredential import EducationalOccupationalCredential
    from msgspec_schemaorg.models.creativework.Syllabus import Syllabus
    from msgspec_schemaorg.models.event.CourseInstance import CourseInstance
    from msgspec_schemaorg.models.intangible.AlignmentObject import AlignmentObject
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.Language import Language
    from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
from typing import Optional, Union, Dict, List, Any


class Course(LearningResource):
    """A description of an educational course which may be offered as distinct instances which take place at different times or take place at different locations, or be offered through different media or modes of study. An educational course is a sequence of one or more educational events and/or creative works which aims to build knowledge, competence or ability of learners."""
    type: str = field(default_factory=lambda: "Course", name="@type")
    numberOfCredits: Union[List[Union[int, 'StructuredValue']], Union[int, 'StructuredValue'], None] = None
    educationalCredentialAwarded: Union[List[Union['URL', str, 'EducationalOccupationalCredential']], Union['URL', str, 'EducationalOccupationalCredential'], None] = None
    hasCourseInstance: Union[List['CourseInstance'], 'CourseInstance', None] = None
    financialAidEligible: Union[List[Union[str, 'DefinedTerm']], Union[str, 'DefinedTerm'], None] = None
    syllabusSections: Union[List['Syllabus'], 'Syllabus', None] = None
    coursePrerequisites: Union[List[Union[str, 'AlignmentObject', 'Course']], Union[str, 'AlignmentObject', 'Course'], None] = None
    occupationalCredentialAwarded: Union[List[Union['URL', str, 'EducationalOccupationalCredential']], Union['URL', str, 'EducationalOccupationalCredential'], None] = None
    courseCode: Union[List[str], str, None] = None
    availableLanguage: Union[List[Union[str, 'Language']], Union[str, 'Language'], None] = None
    totalHistoricalEnrollment: Union[List[int], int, None] = None