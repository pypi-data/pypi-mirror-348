from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.MedicalEntity import MedicalEntity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.DrugCostCategory import DrugCostCategory
    from msgspec_schemaorg.models.intangible.QualitativeValue import QualitativeValue
    from msgspec_schemaorg.models.place.AdministrativeArea import AdministrativeArea
from typing import Optional, Union, Dict, List, Any


class DrugCost(MedicalEntity):
    """The cost per unit of a medical drug. Note that this type is not meant to represent the price in an offer of a drug for sale; see the Offer type for that. This type will typically be used to tag wholesale or average retail cost of a drug, or maximum reimbursable cost. Costs of medical drugs vary widely depending on how and where they are paid for, so while this type captures some of the variables, costs should be used with caution by consumers of this schema's markup."""
    type: str = field(default_factory=lambda: "DrugCost", name="@type")
    costCategory: Union[List['DrugCostCategory'], 'DrugCostCategory', None] = None
    costCurrency: Union[List[str], str, None] = None
    drugUnit: Union[List[str], str, None] = None
    costOrigin: Union[List[str], str, None] = None
    applicableLocation: Union[List['AdministrativeArea'], 'AdministrativeArea', None] = None
    costPerUnit: Union[List[Union[int | float, str, 'QualitativeValue']], Union[int | float, str, 'QualitativeValue'], None] = None