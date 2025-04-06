from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator

from app.config import Language, Theme


class CodeSubmission(BaseModel):
    """Schema for code submission data"""

    code: str = Field(..., min_length=1, max_length=5000)
    language: Language = Language.PYTHON
    theme: Theme = Theme.DEFAULT
    font_size: int = Field(14, ge=8, le=32)
    line_numbers: bool = False
    watermark_text: Optional[str] = None

    @validator("code")
    def code_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Code cannot be empty")
        return v


class ImageResponse(BaseModel):
    """Schema for image generation response"""

    image_url: str
    download_url: str
    generated_at: datetime
    settings: dict
