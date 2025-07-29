from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class DominoAttachmentType(BaseModel):
    database: Optional[str] = Field(default=None, description='Database replica ID', examples=['C1257BFF00563DB0'])
    document: Optional[str] = Field(default=None, description='Document UNID', examples=['C1257B7F0058E304C125704A001AED45'])
    filename: Optional[str] = Field(default=None, description='Název souboru', examples=['2020_03_26_OZO_CENIA.pdf'])
