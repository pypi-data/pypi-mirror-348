from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.Substance import Substance
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.MedicalEnumeration import MedicalEnumeration
    from msgspec_schemaorg.models.thing.DrugLegalStatus import DrugLegalStatus
    from msgspec_schemaorg.models.thing.MaximumDoseSchedule import MaximumDoseSchedule
    from msgspec_schemaorg.models.thing.RecommendedDoseSchedule import RecommendedDoseSchedule
from typing import Optional, Union, Dict, List, Any


class DietarySupplement(Substance):
    """A product taken by mouth that contains a dietary ingredient intended to supplement the diet. Dietary ingredients may include vitamins, minerals, herbs or other botanicals, amino acids, and substances such as enzymes, organ tissues, glandulars and metabolites."""
    type: str = field(default_factory=lambda: "DietarySupplement", name="@type")
    isProprietary: Union[List[bool], bool, None] = None
    activeIngredient: Union[List[str], str, None] = None
    safetyConsideration: Union[List[str], str, None] = None
    recommendedIntake: Union[List['RecommendedDoseSchedule'], 'RecommendedDoseSchedule', None] = None
    maximumIntake: Union[List['MaximumDoseSchedule'], 'MaximumDoseSchedule', None] = None
    legalStatus: Union[List[Union[str, 'MedicalEnumeration', 'DrugLegalStatus']], Union[str, 'MedicalEnumeration', 'DrugLegalStatus'], None] = None
    targetPopulation: Union[List[str], str, None] = None
    proprietaryName: Union[List[str], str, None] = None
    nonProprietaryName: Union[List[str], str, None] = None
    mechanismOfAction: Union[List[str], str, None] = None