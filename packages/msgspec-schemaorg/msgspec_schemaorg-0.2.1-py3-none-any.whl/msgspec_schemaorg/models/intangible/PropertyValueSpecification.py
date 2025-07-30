from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.thing.Thing import Thing
from typing import Optional, Union, Dict, List, Any


class PropertyValueSpecification(Intangible):
    """A Property value specification."""
    type: str = field(default_factory=lambda: "PropertyValueSpecification", name="@type")
    valueMaxLength: Union[List[int | float], int | float, None] = None
    readonlyValue: Union[List[bool], bool, None] = None
    valueRequired: Union[List[bool], bool, None] = None
    valueMinLength: Union[List[int | float], int | float, None] = None
    minValue: Union[List[int | float], int | float, None] = None
    multipleValues: Union[List[bool], bool, None] = None
    defaultValue: Union[List[Union[str, 'Thing']], Union[str, 'Thing'], None] = None
    maxValue: Union[List[int | float], int | float, None] = None
    valueName: Union[List[str], str, None] = None
    stepValue: Union[List[int | float], int | float, None] = None
    valuePattern: Union[List[str], str, None] = None