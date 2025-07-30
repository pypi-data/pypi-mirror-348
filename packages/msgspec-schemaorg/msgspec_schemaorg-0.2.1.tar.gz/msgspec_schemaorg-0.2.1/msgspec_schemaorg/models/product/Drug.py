from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.product.Product import Product
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.DrugPregnancyCategory import DrugPregnancyCategory
    from msgspec_schemaorg.enums.intangible.DrugPrescriptionStatus import DrugPrescriptionStatus
    from msgspec_schemaorg.models.intangible.HealthInsurancePlan import HealthInsurancePlan
    from msgspec_schemaorg.models.intangible.MedicalEnumeration import MedicalEnumeration
    from msgspec_schemaorg.models.product.Drug import Drug
    from msgspec_schemaorg.models.thing.DoseSchedule import DoseSchedule
    from msgspec_schemaorg.models.thing.DrugClass import DrugClass
    from msgspec_schemaorg.models.thing.DrugLegalStatus import DrugLegalStatus
    from msgspec_schemaorg.models.thing.DrugStrength import DrugStrength
    from msgspec_schemaorg.models.thing.MaximumDoseSchedule import MaximumDoseSchedule
from typing import Optional, Union, Dict, List, Any


class Drug(Product):
    """A chemical or biologic substance, used as a medical therapy, that has a physiological effect on an organism. Here the term drug is used interchangeably with the term medicine although clinical knowledge makes a clear difference between them."""
    type: str = field(default_factory=lambda: "Drug", name="@type")
    isProprietary: Union[List[bool], bool, None] = None
    activeIngredient: Union[List[str], str, None] = None
    pregnancyWarning: Union[List[str], str, None] = None
    foodWarning: Union[List[str], str, None] = None
    relatedDrug: Union[List['Drug'], 'Drug', None] = None
    clinicalPharmacology: Union[List[str], str, None] = None
    alcoholWarning: Union[List[str], str, None] = None
    drugClass: Union[List['DrugClass'], 'DrugClass', None] = None
    dosageForm: Union[List[str], str, None] = None
    interactingDrug: Union[List['Drug'], 'Drug', None] = None
    availableStrength: Union[List['DrugStrength'], 'DrugStrength', None] = None
    maximumIntake: Union[List['MaximumDoseSchedule'], 'MaximumDoseSchedule', None] = None
    rxcui: Union[List[str], str, None] = None
    administrationRoute: Union[List[str], str, None] = None
    prescriptionStatus: Union[List[Union[str, 'DrugPrescriptionStatus']], Union[str, 'DrugPrescriptionStatus'], None] = None
    drugUnit: Union[List[str], str, None] = None
    legalStatus: Union[List[Union[str, 'MedicalEnumeration', 'DrugLegalStatus']], Union[str, 'MedicalEnumeration', 'DrugLegalStatus'], None] = None
    pregnancyCategory: Union[List['DrugPregnancyCategory'], 'DrugPregnancyCategory', None] = None
    warning: Union[List[Union['URL', str]], Union['URL', str], None] = None
    overdosage: Union[List[str], str, None] = None
    isAvailableGenerically: Union[List[bool], bool, None] = None
    breastfeedingWarning: Union[List[str], str, None] = None
    proprietaryName: Union[List[str], str, None] = None
    includedInHealthInsurancePlan: Union[List['HealthInsurancePlan'], 'HealthInsurancePlan', None] = None
    labelDetails: Union[List['URL'], 'URL', None] = None
    prescribingInfo: Union[List['URL'], 'URL', None] = None
    doseSchedule: Union[List['DoseSchedule'], 'DoseSchedule', None] = None
    nonProprietaryName: Union[List[str], str, None] = None
    clincalPharmacology: Union[List[str], str, None] = None
    mechanismOfAction: Union[List[str], str, None] = None