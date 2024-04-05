from fastapi import APIRouter, Depends, HTTPException, status
from .... import schemas, crud
from ....utils.oauth2 import get_current_user

router = APIRouter(
    prefix="/accounts", tags=["Accounts"],
    dependencies=[Depends(get_current_user)]
    )

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.AccountInResponse)
async def create_user_account(
    user: schemas.UserInResponse = Depends(get_current_user)
):
    existing_account = crud.accounts_crud.get_by_user_id(
        user_id=user.id,
        raise_error=False,
        )
    if existing_account:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This user already has an account linked to them",
        )
    user_account = schemas.AccountCreate(
        user_id=user.id,
        balance=0.0,
    )
    return crud.accounts_crud.create(obj_in=user_account)

@router.get("/{id}", response_model=schemas.AccountInResponse)
async def get_account_by_id(id: schemas.PyObjectId):
    return crud.accounts_crud.get_by_id(id=id)

@router.put("/{id}", response_model=schemas.AccountInResponse)
async def update_account(id: schemas.PyObjectId, account: schemas.AccountInUpdate):
    return crud.accounts_crud.update(id=id, obj_in=account)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(id: schemas.PyObjectId):
    return crud.accounts_crud.delete(id=id)
