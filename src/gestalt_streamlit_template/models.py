from pathlib import Path
from typing import Optional
from pydantic import BaseModel


class SourceRef(BaseModel):
    lecture_title: str | None
    lecture_summary: str | None
    source_pdf: Path | str
    page: Optional[int]
