from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Dataset import Dataset
    from msgspec_schemaorg.models.intangible.DefinedTerm import DefinedTerm
    from msgspec_schemaorg.enums.intangible.MeasurementMethodEnum import MeasurementMethodEnum
from typing import Optional, Union, Dict, List, Any


class DataCatalog(CreativeWork):
    """A collection of datasets."""
    type: str = field(default_factory=lambda: "DataCatalog", name="@type")
    measurementTechnique: Union[List[Union['URL', str, 'DefinedTerm', 'MeasurementMethodEnum']], Union['URL', str, 'DefinedTerm', 'MeasurementMethodEnum'], None] = None
    measurementMethod: Union[List[Union['URL', str, 'DefinedTerm', 'MeasurementMethodEnum']], Union['URL', str, 'DefinedTerm', 'MeasurementMethodEnum'], None] = None
    dataset: Union[List['Dataset'], 'Dataset', None] = None