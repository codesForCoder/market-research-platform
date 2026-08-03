from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field


class GlobalErrorResponse(BaseModel):
    status: str = "error"
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    error_code: str
    message: str
    details: Any | None = None  # Holds validation breakdowns or debug items
