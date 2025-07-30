from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.creativework.MusicComposition import MusicComposition
    from msgspec_schemaorg.models.creativework.MusicRecording import MusicRecording
    from msgspec_schemaorg.models.event.Event import Event
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class MusicComposition(CreativeWork):
    """A musical composition."""
    type: str = field(default_factory=lambda: "MusicComposition", name="@type")
    musicCompositionForm: Union[List[str], str, None] = None
    lyricist: Union[List['Person'], 'Person', None] = None
    musicArrangement: Union[List['MusicComposition'], 'MusicComposition', None] = None
    iswcCode: Union[List[str], str, None] = None
    musicalKey: Union[List[str], str, None] = None
    recordedAs: Union[List['MusicRecording'], 'MusicRecording', None] = None
    includedComposition: Union[List['MusicComposition'], 'MusicComposition', None] = None
    firstPerformance: Union[List['Event'], 'Event', None] = None
    lyrics: Union[List['CreativeWork'], 'CreativeWork', None] = None
    composer: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None