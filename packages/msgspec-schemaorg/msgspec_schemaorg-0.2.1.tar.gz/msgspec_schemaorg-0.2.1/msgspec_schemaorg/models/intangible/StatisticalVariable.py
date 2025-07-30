from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.ConstraintNode import ConstraintNode
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Class import Class
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.models.intangible.Enumeration import Enumeration
    from msgspec_schemaorg.enums.intangible.MeasurementMethodEnum import MeasurementMethodEnum
    from msgspec_schemaorg.models.intangible.Property import Property
    from msgspec_schemaorg.models.intangible.StatisticalVariable import StatisticalVariable
from typing import Optional, Union, Dict, List, Any


class StatisticalVariable(ConstraintNode):
    """[[StatisticalVariable]] represents any type of statistical metric that can be measured at a place and time. The usage pattern for [[StatisticalVariable]] is typically expressed using [[Observation]] with an explicit [[populationType]], which is a type, typically drawn from Schema.org. Each [[StatisticalVariable]] is marked as a [[ConstraintNode]], meaning that some properties (those listed using [[constraintProperty]]) serve in this setting solely to define the statistical variable rather than literally describe a specific person, place or thing. For example, a [[StatisticalVariable]] Median_Height_Person_Female representing the median height of women, could be written as follows: the population type is [[Person]]; the measuredProperty [[height]]; the [[statType]] [[median]]; the [[gender]] [[Female]]. It is important to note that there are many kinds of scientific quantitative observation which are not fully, perfectly or unambiguously described following this pattern, or with solely Schema.org terminology. The approach taken here is designed to allow partial, incremental or minimal description of [[StatisticalVariable]]s, and the use of detailed sets of entity and property IDs from external repositories. The [[measurementMethod]], [[unitCode]] and [[unitText]] properties can also be used to clarify the specific nature and notation of an observed measurement. """
    type: str = field(default_factory=lambda: "StatisticalVariable", name="@type")
    measuredProperty: Union[List['Property'], 'Property', None] = None
    statType: Union[List[Union['URL', str, 'Property']], Union['URL', str, 'Property'], None] = None
    measurementTechnique: Union[List[Union['URL', str, 'DefinedTerm', 'MeasurementMethodEnum']], Union['URL', str, 'DefinedTerm', 'MeasurementMethodEnum'], None] = None
    measurementDenominator: Union[List['StatisticalVariable'], 'StatisticalVariable', None] = None
    measurementMethod: Union[List[Union['URL', str, 'DefinedTerm', 'MeasurementMethodEnum']], Union['URL', str, 'DefinedTerm', 'MeasurementMethodEnum'], None] = None
    populationType: Union[List['Class'], 'Class', None] = None
    measurementQualifier: Union[List['Enumeration'], 'Enumeration', None] = None