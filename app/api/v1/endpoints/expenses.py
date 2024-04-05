from fastapi import APIRouter, Depends, HTTPException, status
from .... import schemas, crud
from ....utils.oauth2 import get_current_user

router = APIRouter(
    prefix="/expenses", tags=["Expenses"],
    dependencies=[Depends(get_current_user)]
    )

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.ExpenseInResponse)
async def create_user_Expense(
    expense: schemas.ExpenseCreate,
    user: schemas.UserInResponse = Depends(get_current_user)
):
    user_expense = schemas.ExtendedExpenseCreate(
        **expense.__dict__,
        user_id=user.id,
        is_settled=True,
    )
    user_account = schemas.AccountInResponse(**crud.accounts_crud.get_by_user_id(
        user_id=user.id
    ))
    balance = user_account.balance
    if expense.value > balance:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Your balance is too low to settle this Expense"
        )
    new_balance = balance - expense.value
    crud.accounts_crud.update(
        id=user_account.id,
        obj_in=schemas.AccountInUpdate(balance=new_balance)
        )
    return crud.expenses_crud.create(obj_in=user_expense)

@router.get("/{id}", response_model=schemas.ExpenseInResponse)
async def get_Expense_by_id(id: schemas.PyObjectId):
    return crud.expenses_crud.get_by_id(id=id)

@router.put("/{id}", response_model=schemas.ExpenseInResponse)
async def update_Expense(id: schemas.PyObjectId, expense: schemas.ExpenseInUpdate):
    return crud.expenses_crud.update(id=id, obj_in=expense)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_Expense(id: schemas.PyObjectId):
    return crud.expenses_crud.delete(id=id)
