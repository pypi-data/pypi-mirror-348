from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalStudy import MedicalStudy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.MedicalObservationalStudyDesign import MedicalObservationalStudyDesign
from typing import Optional, Union, Dict, List, Any


class MedicalObservationalStudy(MedicalStudy):
    """An observational study is a type of medical study that attempts to infer the possible effect of a treatment through observation of a cohort of subjects over a period of time. In an observational study, the assignment of subjects into treatment groups versus control groups is outside the control of the investigator. This is in contrast with controlled studies, such as the randomized controlled trials represented by MedicalTrial, where each subject is randomly assigned to a treatment group or a control group before the start of the treatment."""
    type: str = field(default_factory=lambda: "MedicalObservationalStudy", name="@type")
    studyDesign: Union[List['MedicalObservationalStudyDesign'], 'MedicalObservationalStudyDesign', None] = None