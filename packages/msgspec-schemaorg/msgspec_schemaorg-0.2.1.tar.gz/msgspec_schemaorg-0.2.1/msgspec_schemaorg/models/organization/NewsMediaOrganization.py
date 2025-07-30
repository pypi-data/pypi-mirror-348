from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.organization.Organization import Organization
from msgspec_schemaorg.utils import URL
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.AboutPage import AboutPage
    from msgspec_schemaorg.models.creativework.Article import Article
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import Optional, Union, Dict, List, Any


class NewsMediaOrganization(Organization):
    """A News/Media organization such as a newspaper or TV station."""
    type: str = field(default_factory=lambda: "NewsMediaOrganization", name="@type")
    diversityPolicy: Union[List[Union['URL', 'CreativeWork']], Union['URL', 'CreativeWork'], None] = None
    unnamedSourcesPolicy: Union[List[Union['URL', 'CreativeWork']], Union['URL', 'CreativeWork'], None] = None
    actionableFeedbackPolicy: Union[List[Union['URL', 'CreativeWork']], Union['URL', 'CreativeWork'], None] = None
    noBylinesPolicy: Union[List[Union['URL', 'CreativeWork']], Union['URL', 'CreativeWork'], None] = None
    ownershipFundingInfo: Union[List[Union['URL', str, 'AboutPage', 'CreativeWork']], Union['URL', str, 'AboutPage', 'CreativeWork'], None] = None
    correctionsPolicy: Union[List[Union['URL', 'CreativeWork']], Union['URL', 'CreativeWork'], None] = None
    verificationFactCheckingPolicy: Union[List[Union['URL', 'CreativeWork']], Union['URL', 'CreativeWork'], None] = None
    masthead: Union[List[Union['URL', 'CreativeWork']], Union['URL', 'CreativeWork'], None] = None
    diversityStaffingReport: Union[List[Union['URL', 'Article']], Union['URL', 'Article'], None] = None
    missionCoveragePrioritiesPolicy: Union[List[Union['URL', 'CreativeWork']], Union['URL', 'CreativeWork'], None] = None
    ethicsPolicy: Union[List[Union['URL', 'CreativeWork']], Union['URL', 'CreativeWork'], None] = None