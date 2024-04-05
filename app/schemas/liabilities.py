from datetime import date
from pydantic import BaseModel, Field
from typing import Optional

from app.schemas.base import DateMixins, PyObjectId

class LiabilityCreate(BaseModel):
    name: str
    category: str
    description: Optional[str] = None
    value: Optional[float] = 0.0

class ExtendedLiabilityCreate(LiabilityCreate, DateMixins):
    user_id: PyObjectId
    is_settled: Optional[bool] = False
    major_categorization: Optional[str] = "liabilities"
    date: Optional[str] = date.today().strftime("%Y-%m-%d")

class LiabilityInResponse(ExtendedLiabilityCreate):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

class LiabilityInUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    value: Optional[float] = None
    is_settled: Optional[float] = None
    date: Optional[str] = date.today().strftime("%Y-%m-%d")