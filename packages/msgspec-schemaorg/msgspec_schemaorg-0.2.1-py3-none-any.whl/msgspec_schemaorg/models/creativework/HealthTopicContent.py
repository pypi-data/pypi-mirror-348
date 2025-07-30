from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.WebContent import WebContent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.enums.intangible.HealthAspectEnumeration import HealthAspectEnumeration
from typing import Optional, Union, Dict, List, Any


class HealthTopicContent(WebContent):
    """[[HealthTopicContent]] is [[WebContent]] that is about some aspect of a health topic, e.g. a condition, its symptoms or treatments. Such content may be comprised of several parts or sections and use different types of media. Multiple instances of [[WebContent]] (and hence [[HealthTopicContent]]) can be related using [[hasPart]] / [[isPartOf]] where there is some kind of content hierarchy, and their content described with [[about]] and [[mentions]] e.g. building upon the existing [[MedicalCondition]] vocabulary.
  """
    type: str = field(default_factory=lambda: "HealthTopicContent", name="@type")
    hasHealthAspect: Union[List['HealthAspectEnumeration'], 'HealthAspectEnumeration', None] = None