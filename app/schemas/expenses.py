from datetime import date
from pydantic import BaseModel, Field
from typing import Optional

from .base import DateMixins, PyObjectId

class ExpenseCreate(BaseModel):
    name: str
    category: str
    description: Optional[str] = None
    value: Optional[float] = 0.0

class ExtendedExpenseCreate(ExpenseCreate, DateMixins):
    user_id: PyObjectId
    is_settled: Optional[bool] = False
    major_categorization: Optional[str] = "expenses"
    date: Optional[str] = date.today().strftime("%Y-%m-%d")

class ExpenseInResponse(ExtendedExpenseCreate):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

class ExpenseInUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    value: Optional[float] = None
    is_settled: Optional[bool] = None
    date: Optional[str] = date.today().strftime("%Y-%m-%d")
