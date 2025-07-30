from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Course import Course
    from msgspec_schemaorg.models.creativework.EducationalOccupationalCredential import EducationalOccupationalCredential
    from msgspec_schemaorg.models.intangible.AlignmentObject import AlignmentObject
    from msgspec_schemaorg.models.intangible.CategoryCode import CategoryCode
    from msgspec_schemaorg.enums.intangible.DayOfWeek import DayOfWeek
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.Demand import Demand
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.MonetaryAmountDistribution import MonetaryAmountDistribution
    from msgspec_schemaorg.models.intangible.Offer import Offer
    from msgspec_schemaorg.models.intangible.StructuredValue import StructuredValue
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class EducationalOccupationalProgram(Intangible):
    """A program offered by an institution which determines the learning progress to achieve an outcome, usually a credential like a degree or certificate. This would define a discrete set of opportunities (e.g., job, courses) that together constitute a program with a clear start, end, set of requirements, and transition to a new occupational opportunity (e.g., a job), or sometimes a higher educational opportunity (e.g., an advanced degree)."""
    type: str = field(default_factory=lambda: "EducationalOccupationalProgram", name="@type")
    termDuration: Union[List['Duration'], 'Duration', None] = None
    numberOfCredits: Union[List[Union[int, 'StructuredValue']], Union[int, 'StructuredValue'], None] = None
    applicationStartDate: Union[List[date], date, None] = None
    offers: Union[List[Union['Demand', 'Offer']], Union['Demand', 'Offer'], None] = None
    educationalCredentialAwarded: Union[List[Union['URL', str, 'EducationalOccupationalCredential']], Union['URL', str, 'EducationalOccupationalCredential'], None] = None
    dayOfWeek: Union[List['DayOfWeek'], 'DayOfWeek', None] = None
    provider: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    financialAidEligible: Union[List[Union[str, 'DefinedTerm']], Union[str, 'DefinedTerm'], None] = None
    programPrerequisites: Union[List[Union[str, 'EducationalOccupationalCredential', 'AlignmentObject', 'Course']], Union[str, 'EducationalOccupationalCredential', 'AlignmentObject', 'Course'], None] = None
    endDate: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    hasCourse: Union[List['Course'], 'Course', None] = None
    occupationalCategory: Union[List[Union[str, 'CategoryCode']], Union[str, 'CategoryCode'], None] = None
    typicalCreditsPerTerm: Union[List[Union[int, 'StructuredValue']], Union[int, 'StructuredValue'], None] = None
    startDate: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    occupationalCredentialAwarded: Union[List[Union['URL', str, 'EducationalOccupationalCredential']], Union['URL', str, 'EducationalOccupationalCredential'], None] = None
    maximumEnrollment: Union[List[int], int, None] = None
    timeToComplete: Union[List['Duration'], 'Duration', None] = None
    applicationDeadline: Union[List[Union[date, str]], Union[date, str], None] = None
    timeOfDay: Union[List[str], str, None] = None
    trainingSalary: Union[List['MonetaryAmountDistribution'], 'MonetaryAmountDistribution', None] = None
    programType: Union[List[Union[str, 'DefinedTerm']], Union[str, 'DefinedTerm'], None] = None
    termsPerYear: Union[List[int | float], int | float, None] = None
    salaryUponCompletion: Union[List['MonetaryAmountDistribution'], 'MonetaryAmountDistribution', None] = None
    educationalProgramMode: Union[List[Union['URL', str]], Union['URL', str], None] = None