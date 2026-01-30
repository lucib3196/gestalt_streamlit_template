

from pathlib import Path
from typing import Optional
from pydantic import BaseModel

class SourceRef(BaseModel):
    source_id: str
    title: str
    path: Path
    page: Optional[int]
    type: str