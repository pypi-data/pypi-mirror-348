from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.intangible.Intangible import Intangible
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.event.Event import Event
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
    from msgspec_schemaorg.models.product.Product import Product
    from msgspec_schemaorg.models.thing.BioChemEntity import BioChemEntity
    from msgspec_schemaorg.models.thing.MedicalEntity import MedicalEntity
from typing import Optional, Union, Dict, List, Any


class Grant(Intangible):
    """A grant, typically financial or otherwise quantifiable, of resources. Typically a [[funder]] sponsors some [[MonetaryAmount]] to an [[Organization]] or [[Person]],
    sometimes not necessarily via a dedicated or long-lived [[Project]], resulting in one or more outputs, or [[fundedItem]]s. For financial sponsorship, indicate the [[funder]] of a [[MonetaryGrant]]. For non-financial support, indicate [[sponsor]] of [[Grant]]s of resources (e.g. office space).

Grants support  activities directed towards some agreed collective goals, often but not always organized as [[Project]]s. Long-lived projects are sometimes sponsored by a variety of grants over time, but it is also common for a project to be associated with a single grant.

The amount of a [[Grant]] is represented using [[amount]] as a [[MonetaryAmount]].
    """
    type: str = field(default_factory=lambda: "Grant", name="@type")
    fundedItem: Union[List[Union['Organization', 'CreativeWork', 'Person', 'Product', 'BioChemEntity', 'MedicalEntity', 'Event']], Union['Organization', 'CreativeWork', 'Person', 'Product', 'BioChemEntity', 'MedicalEntity', 'Event'], None] = None
    sponsor: Union[List[Union['Person', 'Organization']], Union['Person', 'Organization'], None] = None
    funder: Union[List[Union['Organization', 'Person']], Union['Organization', 'Person'], None] = None