from fastapi import APIRouter, Depends, HTTPException, status
from .... import schemas, crud
from ....utils.oauth2 import get_current_user

router = APIRouter(
    prefix="/income", tags=["Income"],
    dependencies=[Depends(get_current_user)]
    )

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.IncomeInResponse)
async def create_user_Income(
    income: schemas.IncomeCreate,
    user: schemas.UserInResponse = Depends(get_current_user)
):
    user_income = schemas.ExtendedIncomeCreate(
        **income.__dict__,
        user_id=user.id,
    )
    user_account = schemas.AccountInResponse(**crud.accounts_crud.get_by_user_id(
        user_id=user.id
    ))
    
    balance = user_account.balance
    new_balance = balance + income.value
    crud.accounts_crud.update(
        schemas.AccountInUpdate(balance=new_balance)
    )
    return crud.income_crud.create(obj_in=user_income)

@router.get("/{id}", response_model=schemas.IncomeInResponse)
async def get_Income_by_id(id: schemas.PyObjectId):
    return crud.income_crud.get_by_id(id=id)

@router.put("/{id}", response_model=schemas.IncomeInResponse)
async def update_Income(
    id: schemas.PyObjectId,
    income: schemas.IncomeInUpdate,
    user: schemas.UserInResponse = Depends(get_current_user),
    ):
    if income.value:
        existing_Income = schemas.IncomeInResponse(**crud.income_crud.get_by_id(id=id))
        if existing_Income.is_settled:
            user_account = schemas.AccountInResponse(**crud.accounts_crud.get_by_user_id(
                user_id=user.id
            ))
            balance = user_account.balance
            new_balance = (balance - existing_Income.value) + income.value
            crud.accounts_crud.update(
                id=user_account.id,
                obj_in=schemas.AccountInUpdate(balance=new_balance)
                )
    return crud.income_crud.update(id=id, obj_in=income)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_Income(id: schemas.PyObjectId):
    return crud.income_crud.delete(id=id, check_settled=True)
