from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Any
from typing import Annotated, Any
from bson.objectid import ObjectId as _ObjectId
from pydantic import (AfterValidator, GetPydanticSchema,
                      EmailStr, Field,
                      PlainSerializer, WithJsonSchema)


def get_current_timestamp():
    return datetime.utcnow()

PyObjectId = Annotated[
    _ObjectId, 
    AfterValidator(lambda id: PyObjectId(id)),
    PlainSerializer(lambda id: str(id), return_type=str, when_used='json-unless-none'),
    WithJsonSchema({ 'type':'string' }, mode='serialization'),
    WithJsonSchema({ 'type':'string' }, mode='validation'),
    GetPydanticSchema(lambda _s, h: h(Any))
]

class DateMixins(BaseModel):
    created_at: Optional[datetime] = get_current_timestamp()
    updated_at: Optional[datetime] = get_current_timestamp()

class BalanceAccount(DateMixins):
    id: PyObjectId = Field(alias='_id')
    user_id: PyObjectId
    balance: float

class Asset(DateMixins):
    id: PyObjectId = Field(alias='_id')
    user_id: PyObjectId
    asset_type: str
    asset_description:Optional[str]
    value: float
    is_settled: Optional[bool] = False

class Liability(DateMixins):
    id: PyObjectId = Field(alias='_id')
    user_id: PyObjectId
    liability_type: str
    liability_description:Optional[str]
    value: float
    is_settled: Optional[bool] = False

class Expense(DateMixins):
    id: PyObjectId = Field(alias='_id')
    user_id: PyObjectId
    expense_type: str
    expense_description:Optional[str]
    value: float
    is_settled: Optional[bool] = False
    

class Badge(DateMixins):
    id: PyObjectId = Field(alias='_id')
    badge_type: str
    badge_description: str
    badge_url: str


class Goal(DateMixins):
    id: PyObjectId = Field(alias='_id')
    user_id: PyObjectId
    goal_type: str
    goal_description: str
    year: int
    month: int
    closing_value: float


class UserBadge(DateMixins):
    id: PyObjectId = Field(alias='_id')
    user_id: PyObjectId
    badges: List[Badge]