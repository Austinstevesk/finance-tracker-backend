from datetime import date
from pydantic import BaseModel, Field
from typing import Optional

from app.schemas.base import DateMixins, PyObjectId

class BudgetCreate(BaseModel):
    name: str
    category: Optional[str] = None
    description: Optional[str] = None
    frequency: Optional[str] = "monthly"
    value: Optional[float] = 0.0
    start_date: Optional[str] = date.today().strftime("%Y-%m-%d")
    end_date: Optional[str] = date.today().strftime("%Y-%m-%d")

class ExtendedBudgetCreate(BudgetCreate, DateMixins):
    user_id: PyObjectId

class BudgetInResponse(ExtendedBudgetCreate):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

class BudgetInUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    frequency: Optional[str] = None
    value: Optional[float] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
