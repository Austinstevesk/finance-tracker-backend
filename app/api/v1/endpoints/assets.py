from fastapi import APIRouter, Depends, HTTPException, status
from app import schemas, crud
from app.utils.oauth2 import get_current_user

router = APIRouter(
    prefix="/assets", tags=["Assets"],
    dependencies=[Depends(get_current_user)]
    )

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.AssetInResponse)
async def create_user_asset(
    asset: schemas.AssetCreate,
    user: schemas.UserInResponse = Depends(get_current_user)
):
    user_asset = schemas.ExtendedAssetCreate(
        **asset.__dict__,
        user_id=user.id,
    )
    return crud.assets_crud.create(obj_in=user_asset)

@router.get("/{id}", response_model=schemas.AssetInResponse)
async def get_asset_by_id(id: schemas.PyObjectId):
    return crud.assets_crud.get_by_id(id=id)

@router.put("/{id}", response_model=schemas.AssetInResponse)
async def update_asset(
    id: schemas.PyObjectId,
    asset: schemas.AssetInUpdate,
    user: schemas.UserInResponse = Depends(get_current_user),
    ):
    if asset.value:
        existing_asset = schemas.AssetInResponse(**crud.assets_crud.get_by_id(id=id))
        if existing_asset.is_settled:
            user_account = schemas.AccountInResponse(**crud.accounts_crud.get_by_user_id(
                user_id=user.id
            ))
            balance = user_account.balance
            new_balance = (balance - existing_asset.value) + asset.value
            crud.accounts_crud.update(
                id=user_account.id,
                obj_in=schemas.AccountInUpdate(balance=new_balance)
                )
    return crud.assets_crud.update(id=id, obj_in=asset)

@router.put("/{id}/settle", response_model=schemas.AssetInResponse)
async def settle_asset(
    id: schemas.PyObjectId,
    user: schemas.UserInResponse = Depends(get_current_user),
    ):
    existing_asset = schemas.AssetInResponse(**crud.assets_crud.get_by_id(id=id))
    # update account balance
    user_account = schemas.AccountInResponse(**crud.accounts_crud.get_by_user_id(
        user_id=user.id
    ))
    balance = user_account.balance
    new_balance = balance + existing_asset.value
    crud.accounts_crud.update(
        id=user_account.id,
        obj_in=schemas.AccountInUpdate(balance=new_balance)
        )
    return crud.assets_crud.update(
        id=id,
        obj_in=schemas.AssetInUpdate(is_settled=True)
        )

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_asset(id: schemas.PyObjectId):
    return crud.assets_crud.delete(id=id, check_settled=True)
