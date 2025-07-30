from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalEntity import MedicalEntity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.EventStatusType import EventStatusType
    from msgspec_schemaorg.enums.intangible.MedicalStudyStatus import MedicalStudyStatus
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.place.AdministrativeArea import AdministrativeArea
    from msgspec_schemaorg.models.thing.MedicalCondition import MedicalCondition
    from msgspec_schemaorg.models.thing.MedicalEntity import MedicalEntity
from typing import Optional, Union, Dict, List, Any


class MedicalStudy(MedicalEntity):
    """A medical study is an umbrella type covering all kinds of research studies relating to human medicine or health, including observational studies and interventional trials and registries, randomized, controlled or not. When the specific type of study is known, use one of the extensions of this type, such as MedicalTrial or MedicalObservationalStudy. Also, note that this type should be used to mark up data that describes the study itself; to tag an article that publishes the results of a study, use MedicalScholarlyArticle. Note: use the code property of MedicalEntity to store study IDs, e.g. clinicaltrials.gov ID."""
    type: str = field(default_factory=lambda: "MedicalStudy", name="@type")
    status: Union[List[Union[str, 'MedicalStudyStatus', 'EventStatusType']], Union[str, 'MedicalStudyStatus', 'EventStatusType'], None] = None
    studyLocation: Union[List['AdministrativeArea'], 'AdministrativeArea', None] = None
    studySubject: Union[List['MedicalEntity'], 'MedicalEntity', None] = None
    healthCondition: Union[List['MedicalCondition'], 'MedicalCondition', None] = None
    sponsor: Union[List[Union['Person', 'Organization']], Union['Person', 'Organization'], None] = None