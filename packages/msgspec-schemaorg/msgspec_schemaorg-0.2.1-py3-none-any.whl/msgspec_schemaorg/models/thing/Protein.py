from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.thing.BioChemEntity import BioChemEntity
from typing import Optional, Union, Dict, List, Any


class Protein(BioChemEntity):
    """Protein is here used in its widest possible definition, as classes of amino acid based molecules. Amyloid-beta Protein in human (UniProt P05067), eukaryota (e.g. an OrthoDB group) or even a single molecule that one can point to are all of type :Protein. A protein can thus be a subclass of another protein, e.g. :Protein as a UniProt record can have multiple isoforms inside it which would also be :Protein. They can be imagined, synthetic, hypothetical or naturally occurring."""
    type: str = field(default_factory=lambda: "Protein", name="@type")
    hasBioPolymerSequence: Union[List[str], str, None] = None