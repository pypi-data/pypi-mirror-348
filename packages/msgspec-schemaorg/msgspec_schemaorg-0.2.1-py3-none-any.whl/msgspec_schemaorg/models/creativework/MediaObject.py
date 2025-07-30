from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from msgspec_schemaorg.utils import parse_iso8601
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.Claim import Claim
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.creativework.NewsArticle import NewsArticle
    from msgspec_schemaorg.models.intangible.Distance import Distance
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.GeoShape import GeoShape
    from msgspec_schemaorg.models.intangible.MediaSubscription import MediaSubscription
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.place.Place import Place
from datetime import date, datetime, time
from typing import Optional, Union, Dict, List, Any


class MediaObject(CreativeWork):
    """A media object, such as an image, video, audio, or text object embedded in a web page or a downloadable dataset i.e. DataDownload. Note that a creative work may have many media objects associated with it on the same web page. For example, a page about a single song (MusicRecording) may have a music video (VideoObject), and a high and low bandwidth audio stream (2 AudioObject's)."""
    type: str = field(default_factory=lambda: "MediaObject", name="@type")
    startTime: Union[List[Union[datetime, time]], Union[datetime, time], None] = None
    bitrate: Union[List[str], str, None] = None
    duration: Union[List[Union['QuantitativeValue', 'Duration']], Union['QuantitativeValue', 'Duration'], None] = None
    encodesCreativeWork: Union[List['CreativeWork'], 'CreativeWork', None] = None
    contentUrl: Union[List['URL'], 'URL', None] = None
    uploadDate: Union[List[Union[datetime, date]], Union[datetime, date], None] = None
    height: Union[List[Union['Distance', 'QuantitativeValue']], Union['Distance', 'QuantitativeValue'], None] = None
    encodingFormat: Union[List[Union['URL', str]], Union['URL', str], None] = None
    embedUrl: Union[List['URL'], 'URL', None] = None
    requiresSubscription: Union[List[Union[bool, 'MediaSubscription']], Union[bool, 'MediaSubscription'], None] = None
    ineligibleRegion: Union[List[Union[str, 'Place', 'GeoShape']], Union[str, 'Place', 'GeoShape'], None] = None
    playerType: Union[List[str], str, None] = None
    width: Union[List[Union['Distance', 'QuantitativeValue']], Union['Distance', 'QuantitativeValue'], None] = None
    endTime: Union[List[Union[datetime, time]], Union[datetime, time], None] = None
    regionsAllowed: Union[List['Place'], 'Place', None] = None
    contentSize: Union[List[str], str, None] = None
    sha256: Union[List[str], str, None] = None
    associatedArticle: Union[List['NewsArticle'], 'NewsArticle', None] = None
    productionCompany: Union[List['Organization'], 'Organization', None] = None
    interpretedAsClaim: Union[List['Claim'], 'Claim', None] = None