from pydantic import BaseModel, Field
from typing import Optional
from .base import PyObjectId, DateMixins

class Account(BaseModel):
    balance: Optional[float] = float

class AccountCreate(Account, DateMixins):
    user_id: PyObjectId

class AccountInResponse(AccountCreate):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId

class AccountInUpdate(Account):
    pass

