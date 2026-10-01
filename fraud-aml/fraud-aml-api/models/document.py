"""Knowledge document API models."""

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


DocumentType = Literal[
    "typology_guide",
    "investigation_procedure",
    "sanctions_guidance",
    "sar_procedure",
    "false_positive_case_note",
]


class Document(BaseModel):
    document_id: str
    title: str = Field(min_length=1)
    document_type: DocumentType
    content: str = Field(min_length=1)
    created_at: date
