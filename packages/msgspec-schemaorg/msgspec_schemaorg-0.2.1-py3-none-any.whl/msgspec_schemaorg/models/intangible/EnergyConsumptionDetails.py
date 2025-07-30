from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.EUEnergyEfficiencyEnumeration import EUEnergyEfficiencyEnumeration
    from msgspec_schemaorg.models.intangible.EnergyEfficiencyEnumeration import EnergyEfficiencyEnumeration
from typing import Optional, Union, Dict, List, Any


class EnergyConsumptionDetails(Intangible):
    """EnergyConsumptionDetails represents information related to the energy efficiency of a product that consumes energy. The information that can be provided is based on international regulations such as for example [EU directive 2017/1369](https://eur-lex.europa.eu/eli/reg/2017/1369/oj) for energy labeling and the [Energy labeling rule](https://www.ftc.gov/enforcement/rules/rulemaking-regulatory-reform-proceedings/energy-water-use-labeling-consumer) under the Energy Policy and Conservation Act (EPCA) in the US."""
    type: str = field(default_factory=lambda: "EnergyConsumptionDetails", name="@type")
    hasEnergyEfficiencyCategory: Union[List['EnergyEfficiencyEnumeration'], 'EnergyEfficiencyEnumeration', None] = None
    energyEfficiencyScaleMax: Union[List['EUEnergyEfficiencyEnumeration'], 'EUEnergyEfficiencyEnumeration', None] = None
    energyEfficiencyScaleMin: Union[List['EUEnergyEfficiencyEnumeration'], 'EUEnergyEfficiencyEnumeration', None] = None