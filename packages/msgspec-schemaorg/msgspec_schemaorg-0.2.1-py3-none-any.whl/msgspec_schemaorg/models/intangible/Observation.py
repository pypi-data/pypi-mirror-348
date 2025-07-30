from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
    from msgspec_schemaorg.enums.intangible.MeasurementMethodEnum import MeasurementMethodEnum
    from msgspec_schemaorg.models.intangible.Property import Property
    from msgspec_schemaorg.models.intangible.PropertyValue import PropertyValue
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.intangible.StatisticalVariable import StatisticalVariable
    from msgspec_schemaorg.models.place.Place import Place
    from msgspec_schemaorg.models.thing.Thing import Thing
from datetime import datetime
from typing import Optional, Union, Dict, List, Any


class Observation(Intangible):
    """Instances of the class [[Observation]] are used to specify observations about an entity at a particular time. The principal properties of an [[Observation]] are [[observationAbout]], [[measuredProperty]], [[statType]], [[value] and [[observationDate]]  and [[measuredProperty]]. Some but not all Observations represent a [[QuantitativeValue]]. Quantitative observations can be about a [[StatisticalVariable]], which is an abstract specification about which we can make observations that are grounded at a particular location and time.

Observations can also encode a subset of simple RDF-like statements (its observationAbout, a StatisticalVariable, defining the measuredPoperty; its observationAbout property indicating the entity the statement is about, and [[value]] )

In the context of a quantitative knowledge graph, typical properties could include [[measuredProperty]], [[observationAbout]], [[observationDate]], [[value]], [[unitCode]], [[unitText]], [[measurementMethod]].
    """
    type: str = field(default_factory=lambda: "Observation", name="@type")
    marginOfError: Union[List['QuantitativeValue'], 'QuantitativeValue', None] = None
    measuredProperty: Union[List['Property'], 'Property', None] = None
    measurementTechnique: Union[List[Union['URL', str, 'DefinedTerm', 'MeasurementMethodEnum']], Union['URL', str, 'DefinedTerm', 'MeasurementMethodEnum'], None] = None
    measurementDenominator: Union[List['StatisticalVariable'], 'StatisticalVariable', None] = None
    measurementMethod: Union[List[Union['URL', str, 'DefinedTerm', 'MeasurementMethodEnum']], Union['URL', str, 'DefinedTerm', 'MeasurementMethodEnum'], None] = None
    observationPeriod: Union[List[str], str, None] = None
    variableMeasured: Union[List[Union[str, 'Property', 'StatisticalVariable', 'PropertyValue']], Union[str, 'Property', 'StatisticalVariable', 'PropertyValue'], None] = None
    observationDate: Union[List[datetime], datetime, None] = None
    observationAbout: Union[List[Union['Place', 'Thing']], Union['Place', 'Thing'], None] = None
    measurementQualifier: Union[List['Enumeration'], 'Enumeration', None] = None