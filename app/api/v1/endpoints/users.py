from fastapi import APIRouter, Depends, status
from typing import List
from .... import schemas, crud
from ....utils.oauth2 import get_current_user

router = APIRouter(
    prefix="/users", tags=["Users"],
    dependencies=[Depends(get_current_user)]
    )

@router.get("/profile", response_model=schemas.UserInResponse)
async def get_user_profile(user: schemas.UserInResponse = Depends(get_current_user)):
    return user

@router.get("/user-account", response_model=schemas.AccountInResponse)
async def get_user_account(user: schemas.UserInResponse = Depends(get_current_user)):
    return crud.accounts_crud.get_by_user_id(user_id=user.id)

@router.get("/user-assets", response_model=List[schemas.AssetInResponse])
async def get_user_assets(user: schemas.UserInResponse = Depends(get_current_user)):
    return crud.assets_crud.get_many_by_user_id(user_id=user.id)

@router.get("/{id}", response_model=schemas.UserInResponse)
async def get_user_by_id(id: schemas.PyObjectId):
    return crud.user_crud.get_by_id(id=id)

@router.put("/{id}", response_model=schemas.UserInResponse)
async def update_user(id: schemas.PyObjectId, user: schemas.UserInUpdate):
    return crud.user_crud.update(id=id, obj_in=user)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: schemas.PyObjectId):
    return crud.user_crud.delete(id=id)