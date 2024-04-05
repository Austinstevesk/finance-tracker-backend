from datetime import date
from pydantic import BaseModel, Field
from typing import Optional

from app.schemas.base import DateMixins, PyObjectId

class GoalCreate(BaseModel):
    name: str
    category: Optional[str] = None
    description: Optional[str] = None
    closing_value: Optional[float] = 0.0
    target_date: Optional[str] = date.today().strftime("%Y-%m-%d")

class ExtendedGoalCreate(GoalCreate, DateMixins):
    user_id: PyObjectId
    is_achieved: Optional[bool] = False

class GoalInResponse(ExtendedGoalCreate):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

class GoalInUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    closing_value: Optional[float] = None
    is_achieved: Optional[bool] = None
    target_date: Optional[str] = None
