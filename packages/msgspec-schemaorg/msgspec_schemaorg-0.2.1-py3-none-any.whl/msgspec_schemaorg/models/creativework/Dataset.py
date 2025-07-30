from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.DataCatalog import DataCatalog
    from msgspec_schemaorg.models.creativework.DataDownload import DataDownload
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.enums.intangible.MeasurementMethodEnum import MeasurementMethodEnum
    from msgspec_schemaorg.models.intangible.Property import Property
    from msgspec_schemaorg.models.intangible.PropertyValue import PropertyValue
    from msgspec_schemaorg.models.intangible.StatisticalVariable import StatisticalVariable
from datetime import datetime
from typing import Optional, Union, Dict, List, Any


class Dataset(CreativeWork):
    """A body of structured information describing some topic(s) of interest."""
    type: str = field(default_factory=lambda: "Dataset", name="@type")
    includedInDataCatalog: Union[List['DataCatalog'], 'DataCatalog', None] = None
    issn: Union[List[str], str, None] = None
    measurementTechnique: Union[List[Union['URL', str, 'DefinedTerm', 'MeasurementMethodEnum']], Union['URL', str, 'DefinedTerm', 'MeasurementMethodEnum'], None] = None
    catalog: Union[List['DataCatalog'], 'DataCatalog', None] = None
    measurementMethod: Union[List[Union['URL', str, 'DefinedTerm', 'MeasurementMethodEnum']], Union['URL', str, 'DefinedTerm', 'MeasurementMethodEnum'], None] = None
    variableMeasured: Union[List[Union[str, 'Property', 'StatisticalVariable', 'PropertyValue']], Union[str, 'Property', 'StatisticalVariable', 'PropertyValue'], None] = None
    distribution: Union[List['DataDownload'], 'DataDownload', None] = None
    includedDataCatalog: Union[List['DataCatalog'], 'DataCatalog', None] = None
    datasetTimeInterval: Union[List[datetime], datetime, None] = None