from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalEntity import MedicalEntity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.EventStatusType import EventStatusType
    from msgspec_schemaorg.enums.intangible.MedicalStudyStatus import MedicalStudyStatus
    from msgspec_schemaorg.models.product.Drug import Drug
    from msgspec_schemaorg.models.thing.AnatomicalStructure import AnatomicalStructure
    from msgspec_schemaorg.models.thing.AnatomicalSystem import AnatomicalSystem
    from msgspec_schemaorg.models.thing.DDxElement import DDxElement
    from msgspec_schemaorg.models.thing.MedicalConditionStage import MedicalConditionStage
    from msgspec_schemaorg.models.thing.MedicalRiskFactor import MedicalRiskFactor
    from msgspec_schemaorg.models.thing.MedicalSignOrSymptom import MedicalSignOrSymptom
    from msgspec_schemaorg.models.thing.MedicalTest import MedicalTest
    from msgspec_schemaorg.models.thing.MedicalTherapy import MedicalTherapy
    from msgspec_schemaorg.models.thing.SuperficialAnatomy import SuperficialAnatomy
from typing import Optional, Union, Dict, List, Any


class MedicalCondition(MedicalEntity):
    """Any condition of the human body that affects the normal functioning of a person, whether physically or mentally. Includes diseases, injuries, disabilities, disorders, syndromes, etc."""
    type: str = field(default_factory=lambda: "MedicalCondition", name="@type")
    primaryPrevention: Union[List['MedicalTherapy'], 'MedicalTherapy', None] = None
    signOrSymptom: Union[List['MedicalSignOrSymptom'], 'MedicalSignOrSymptom', None] = None
    status: Union[List[Union[str, 'MedicalStudyStatus', 'EventStatusType']], Union[str, 'MedicalStudyStatus', 'EventStatusType'], None] = None
    naturalProgression: Union[List[str], str, None] = None
    stage: Union[List['MedicalConditionStage'], 'MedicalConditionStage', None] = None
    riskFactor: Union[List['MedicalRiskFactor'], 'MedicalRiskFactor', None] = None
    secondaryPrevention: Union[List['MedicalTherapy'], 'MedicalTherapy', None] = None
    possibleComplication: Union[List[str], str, None] = None
    expectedPrognosis: Union[List[str], str, None] = None
    possibleTreatment: Union[List['MedicalTherapy'], 'MedicalTherapy', None] = None
    drug: Union[List['Drug'], 'Drug', None] = None
    associatedAnatomy: Union[List[Union['AnatomicalStructure', 'SuperficialAnatomy', 'AnatomicalSystem']], Union['AnatomicalStructure', 'SuperficialAnatomy', 'AnatomicalSystem'], None] = None
    epidemiology: Union[List[str], str, None] = None
    pathophysiology: Union[List[str], str, None] = None
    differentialDiagnosis: Union[List['DDxElement'], 'DDxElement', None] = None
    typicalTest: Union[List['MedicalTest'], 'MedicalTest', None] = None