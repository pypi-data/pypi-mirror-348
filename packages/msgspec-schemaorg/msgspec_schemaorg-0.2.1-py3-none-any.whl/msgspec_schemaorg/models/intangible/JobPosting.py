from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.EducationalOccupationalCredential import EducationalOccupationalCredential
    from msgspec_schemaorg.models.intangible.CategoryCode import CategoryCode
    from msgspec_schemaorg.models.intangible.ContactPoint import ContactPoint
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.MonetaryAmount import MonetaryAmount
    from msgspec_schemaorg.models.intangible.MonetaryAmountDistribution import MonetaryAmountDistribution
    from msgspec_schemaorg.models.intangible.Occupation import Occupation
    from msgspec_schemaorg.models.intangible.OccupationalExperienceRequirements import OccupationalExperienceRequirements
    from msgspec_schemaorg.models.intangible.PriceSpecification import PriceSpecification
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.place.AdministrativeArea import AdministrativeArea
    from msgspec_schemaorg.models.place.Place import Place
from datetime import date, datetime
from typing import Optional, Union, Dict, List, Any


class JobPosting(Intangible):
    """A listing that describes a job opening in a certain organization."""
    type: str = field(default_factory=lambda: "JobPosting", name="@type")
    experienceRequirements: Union[List[Union[str, 'OccupationalExperienceRequirements']], Union[str, 'OccupationalExperienceRequirements'], None] = None
    jobImmediateStart: Union[List[bool], bool, None] = None
    responsibilities: Union[List[str], str, None] = None
    jobStartDate: Union[List[Union[date, str]], Union[date, str], None] = None
    datePosted: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    applicationContact: Union[List['ContactPoint'], 'ContactPoint', None] = None
    benefits: Union[List[str], str, None] = None
    skills: Union[List[Union[str, 'DefinedTerm']], Union[str, 'DefinedTerm'], None] = None
    employerOverview: Union[List[str], str, None] = None
    jobBenefits: Union[List[str], str, None] = None
    directApply: Union[List[bool], bool, None] = None
    workHours: Union[List[str], str, None] = None
    hiringOrganization: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None
    applicantLocationRequirements: Union[List['AdministrativeArea'], 'AdministrativeArea', None] = None
    totalJobOpenings: Union[List[int], int, None] = None
    eligibilityToWorkRequirement: Union[List[str], str, None] = None
    specialCommitments: Union[List[str], str, None] = None
    occupationalCategory: Union[List[Union[str, 'CategoryCode']], Union[str, 'CategoryCode'], None] = None
    incentiveCompensation: Union[List[str], str, None] = None
    jobLocationType: Union[List[str], str, None] = None
    employmentUnit: Union[List['Organization'], 'Organization', None] = None
    employmentType: Union[List[str], str, None] = None
    qualifications: Union[List[Union[str, 'EducationalOccupationalCredential']], Union[str, 'EducationalOccupationalCredential'], None] = None
    experienceInPlaceOfEducation: Union[List[bool], bool, None] = None
    relevantOccupation: Union[List['Occupation'], 'Occupation', None] = None
    educationRequirements: Union[List[Union[str, 'EducationalOccupationalCredential']], Union[str, 'EducationalOccupationalCredential'], None] = None
    estimatedSalary: Union[List[Union[int | float, 'MonetaryAmount', 'MonetaryAmountDistribution']], Union[int | float, 'MonetaryAmount', 'MonetaryAmountDistribution'], None] = None
    baseSalary: Union[List[Union[int | float, 'PriceSpecification', 'MonetaryAmount']], Union[int | float, 'PriceSpecification', 'MonetaryAmount'], None] = None
    incentives: Union[List[str], str, None] = None
    industry: Union[List[Union[str, 'DefinedTerm']], Union[str, 'DefinedTerm'], None] = None
    title: Union[List[str], str, None] = None
    salaryCurrency: Union[List[str], str, None] = None
    sensoryRequirement: Union[List[Union['URL', str, 'DefinedTerm']], Union['URL', str, 'DefinedTerm'], None] = None
    jobLocation: Union[List['Place'], 'Place', None] = None
    securityClearanceRequirement: Union[List[Union['URL', str]], Union['URL', str], None] = None
    physicalRequirement: Union[List[Union['URL', str, 'DefinedTerm']], Union['URL', str, 'DefinedTerm'], None] = None
    validThrough: Union[List[Union[datetime, date]], Union[datetime, date], None] = None