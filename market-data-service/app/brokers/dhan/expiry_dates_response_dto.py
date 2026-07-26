from datetime import date
from pydantic import BaseModel

# 1. Define the structural schema blueprint
class DateResponseSchema(BaseModel):
    data: list[date]  # Automatically validates and parses string dates into real python date objects
    status: str

