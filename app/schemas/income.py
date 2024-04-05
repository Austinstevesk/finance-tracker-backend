from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

from .base import DateMixins, PyObjectId

class IncomeCreate(BaseModel):
    income_source: str
    description: Optional[str] = None
    value: Optional[float] = 0.0
    date_received: Optional[str] = date.today().strftime("%Y-%m-%d")

class ExtendedIncomeCreate(IncomeCreate, DateMixins):
    user_id: PyObjectId

class IncomeInResponse(ExtendedIncomeCreate):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

class IncomeInUpdate(BaseModel):
    income_source: Optional[str] = None
    description: Optional[str] = None
    value: Optional[float] = None
    date_received: Optional[str] = None
