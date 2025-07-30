from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.event.Event import Event
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.intangible.Schedule import Schedule
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class CourseInstance(Event):
    """An instance of a [[Course]] which is distinct from other instances because it is offered at a different time or location or through different media or modes of study or to a specific section of students."""
    type: str = field(default_factory=lambda: "CourseInstance", name="@type")
    instructor: Union[List['Person'], 'Person', None] = None
    courseSchedule: Union[List['Schedule'], 'Schedule', None] = None
    courseWorkload: Union[List[str], str, None] = None
    courseMode: Union[List[Union['URL', str]], Union['URL', str], None] = None