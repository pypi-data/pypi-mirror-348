import enum
from typing import ClassVar, Dict, Any

class PhysicalExam(str, enum.Enum):
    """Schema.org enumeration values for PhysicalExam."""

    Abdomen = "Abdomen"  # "Abdomen clinical examination."
    Appearance = "Appearance"  # "Appearance assessment with clinical examination."
    CardiovascularExam = "CardiovascularExam"  # "Cardiovascular system assessment with clinical examination."
    Ear = "Ear"  # "Ear function assessment with clinical examination."
    Eye = "Eye"  # "Eye or ophthalmological function assessment with clinical..."
    Genitourinary = "Genitourinary"  # "Genitourinary system function assessment with clinical ex..."
    Head = "Head"  # "Head assessment with clinical examination."
    Lung = "Lung"  # "Lung and respiratory system clinical examination."
    MusculoskeletalExam = "MusculoskeletalExam"  # "Musculoskeletal system clinical examination."
    Neck = "Neck"  # "Neck assessment with clinical examination."
    Neuro = "Neuro"  # "Neurological system clinical examination."
    Nose = "Nose"  # "Nose function assessment with clinical examination."
    Skin = "Skin"  # "Skin assessment with clinical examination."
    Throat = "Throat"  # "Throat assessment with  clinical examination."

    # Metadata for each enum value
    metadata: ClassVar[Dict[str, Dict[str, Any]]] = {
        "Abdomen": {
            "id": "schema:Abdomen",
            "comment": """Abdomen clinical examination.""",
            "label": "Abdomen",
        },
        "Appearance": {
            "id": "schema:Appearance",
            "comment": """Appearance assessment with clinical examination.""",
            "label": "Appearance",
        },
        "CardiovascularExam": {
            "id": "schema:CardiovascularExam",
            "comment": """Cardiovascular system assessment with clinical examination.""",
            "label": "CardiovascularExam",
        },
        "Ear": {
            "id": "schema:Ear",
            "comment": """Ear function assessment with clinical examination.""",
            "label": "Ear",
        },
        "Eye": {
            "id": "schema:Eye",
            "comment": """Eye or ophthalmological function assessment with clinical examination.""",
            "label": "Eye",
        },
        "Genitourinary": {
            "id": "schema:Genitourinary",
            "comment": """Genitourinary system function assessment with clinical examination.""",
            "label": "Genitourinary",
        },
        "Head": {
            "id": "schema:Head",
            "comment": """Head assessment with clinical examination.""",
            "label": "Head",
        },
        "Lung": {
            "id": "schema:Lung",
            "comment": """Lung and respiratory system clinical examination.""",
            "label": "Lung",
        },
        "MusculoskeletalExam": {
            "id": "schema:MusculoskeletalExam",
            "comment": """Musculoskeletal system clinical examination.""",
            "label": "MusculoskeletalExam",
        },
        "Neck": {
            "id": "schema:Neck",
            "comment": """Neck assessment with clinical examination.""",
            "label": "Neck",
        },
        "Neuro": {
            "id": "schema:Neuro",
            "comment": """Neurological system clinical examination.""",
            "label": "Neuro",
        },
        "Nose": {
            "id": "schema:Nose",
            "comment": """Nose function assessment with clinical examination.""",
            "label": "Nose",
        },
        "Skin": {
            "id": "schema:Skin",
            "comment": """Skin assessment with clinical examination.""",
            "label": "Skin",
        },
        "Throat": {
            "id": "schema:Throat",
            "comment": """Throat assessment with  clinical examination.""",
            "label": "Throat",
        },
    }