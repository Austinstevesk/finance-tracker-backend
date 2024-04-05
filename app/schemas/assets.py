from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

from .base import DateMixins, PyObjectId

class AssetCreate(BaseModel):
    name: str
    category: Optional[str] = None
    description: Optional[str] = None
    value: Optional[float] = 0.0

class ExtendedAssetCreate(AssetCreate, DateMixins):
    user_id: PyObjectId
    is_settled: Optional[bool] = False
    major_categorization: Optional[str] = "assets"
    date: Optional[str] = date.today().strftime("%Y-%m-%d")

class AssetInResponse(ExtendedAssetCreate):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

class AssetInUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    value: Optional[float] = None
    is_settled: Optional[bool] = None
    date: Optional[str] = date.today().strftime("%Y-%m-%d")
