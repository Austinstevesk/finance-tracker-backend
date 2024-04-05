from fastapi import HTTPException, status, Response
from pydantic import BaseModel
from typing import List
from ..schemas.base import PyObjectId, get_current_timestamp

class CRUDBase:
    def __init__(self, collection, item_str) -> None:
        self.collection = collection
        self.item_str = item_str
    
    def create(self, obj_in: BaseModel) -> dict:
        inserted_item = self.collection.insert_one(obj_in.__dict__)
        id = inserted_item.inserted_id
        created_item = self.collection.find_one({"_id": id})
        return created_item
    
    def get_by_id(self, id: PyObjectId) -> dict | None:
        item = self.collection.find_one({"_id": PyObjectId(id)})
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{self.item_str} not found"
            )
        return item
    
    def get_many(self, query) -> List[dict]:
        items = self.collection.find(query).sort("updated_at")
        return items

    def get_by_user_id(self, user_id: PyObjectId, raise_error: bool = True) -> dict | None:
        item = self.collection.find_one({"user_id": PyObjectId(user_id)})
        if not item:
            if raise_error:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"This user has no {self.item_str.lower()} linked to them"
                )
        return item
    
    def get_many_by_user_id(self, user_id: PyObjectId) -> List[dict] | None:
        query = {"user_id": PyObjectId(user_id)}
        items = self.get_many(query=query)
        return items
    
    def update(self, id: PyObjectId, obj_in: BaseModel, check_settled: bool = False) -> dict:
        existing_item = self.get_by_id(id=id)
        existing_item["updated_at"] = get_current_timestamp()
        if check_settled:
            if existing_item["is_settled"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Cannot update settled {self.item_str.lower()}"
                )
        data = {key: value for key, value in obj_in if value is not None}
        if len(data) > 0:
            for key, value in data.items():
                existing_item[key] = value
        update_result = self.collection.update_one(
                    {"_id": PyObjectId(id)}, {"$set": existing_item}
                )
        if update_result.modified_count == 1:
            if (
                updated_item := self.collection.find_one(
                    {"_id": PyObjectId(id)}
                )
            ) is not None:
                return updated_item
        return existing_item
    
    def delete(self, id: PyObjectId, check_settled: bool = False) -> Response:
        existing_item = self.get_by_id(id=id)
        if check_settled:
            if existing_item["is_settled"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Cannot delete settled {self.item_str.lower()}"
                )
        delete_result = self.collection.delete_one({"_id": PyObjectId(id)})
        if delete_result.deleted_count == 1:
            return Response(status_code=status.HTTP_204_NO_CONTENT)