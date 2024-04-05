from fastapi import APIRouter, Depends, HTTPException, status
from .... import schemas, crud
from ....utils.oauth2 import get_current_user

router = APIRouter(
    prefix="/liabilities", tags=["Liabilities"],
    dependencies=[Depends(get_current_user)]
    )

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.LiabilityInResponse)
async def create_user_liability(
    liability: schemas.LiabilityCreate,
    user: schemas.UserInResponse = Depends(get_current_user)
):
    user_liability = schemas.ExtendedLiabilityCreate(
        **liability.__dict__,
        user_id=user.id,
    )
    return crud.liabilities_crud.create(obj_in=user_liability)

@router.get("/{id}", response_model=schemas.LiabilityInResponse)
async def get_liability_by_id(id: schemas.PyObjectId):
    return crud.liabilities_crud.get_by_id(id=id)

@router.put("/{id}", response_model=schemas.LiabilityInResponse)
async def update_liability(id: schemas.PyObjectId, liability: schemas.LiabilityInUpdate):
    return crud.liabilities_crud.update(id=id, obj_in=liability)

@router.put("/{id}/settle", response_model=schemas.LiabilityInResponse)
async def settle_liability(
    id: schemas.PyObjectId,
    user: schemas.UserInResponse = Depends(get_current_user),
    ):
    existing_liability = schemas.LiabilityInResponse(**crud.liabilities_crud.get_by_id(id=id))
    # update account balance
    user_account = schemas.AccountInResponse(**crud.accounts_crud.get_by_user_id(
        user_id=user.id
    ))
    balance = user_account.balance
    if existing_liability.value > balance:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Your balance is too low to settle this liability"
        )
    new_balance = balance - existing_liability.value
    crud.liabilities_crud.update(
        id=user_account.id,
        obj_in=schemas.AccountInUpdate(balance=new_balance)
        )
    return crud.liabilities_crud.update(
        id=id,
        obj_in=schemas.LiabilityInUpdate(is_settled=True)
        )

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_liability(id: schemas.PyObjectId):
    return crud.liabilities_crud.delete(id=id, check_settled=True)
