from fastapi import APIRouter, Depends, HTTPException, status
from datetime import date, timedelta
from app import schemas, crud
from app.utils.date_utils import get_current_month_min_max_dates
from app.utils.oauth2 import get_current_user

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
    date_today = date.today()
    query =  {
            "user_id": schemas.PyObjectId(user.id),
            "category": user_expense.major_categorization,
            "start_date": {"$gte": date_today.strftime("%Y-%m-%d")},
            "end_date": {"$lte": date_today.strftime("%Y-%m-%d")}
            }
    budget  = crud.budgets_crud.get_by_query(query=query)
    expenses_budget = None
    if budget:
        expenses_budget = schemas.BudgetInResponse(**budget)
    if expenses_budget:
        # get the months expenses
        min_date = date_today.replace(day=1).strftime("%Y-%m-%d")
        max_date = (
            date_today.replace(
                month=date_today.month + 1
                ).replace(day=1) - timedelta(days=1)
            ).strftime("%Y-%m-%d")
        query =  {
            "user_id": schemas.PyObjectId(user.id),
            "major_categorization": "expenses",
            "date": {"$gte": min_date},
            "date": {"$lte": max_date}
            }
        expenses = crud.expenses_crud.get_many(query=query)
        total = 0
        for data in expenses:
            total += data["value"]
        if expenses_budget.value < (total + expense.value):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot settle the expense due to budget constraints"
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

@router.get("/current-month-expenses", response_model=schemas.TotalDisplay)
async def get_current_month_expenses(
    user: schemas.UserInResponse = Depends(get_current_user)
    ):
    min_date, max_date = get_current_month_min_max_dates()
    query = {
        "user_id": schemas.PyObjectId(user.id),
        "date": {"$gte": min_date},
        "date": {"$lte": max_date},
    }
    current_month_expenses = crud.expenses_crud.get_many(
        query=query,
    )
    total = 0
    for exp in current_month_expenses:
        total += exp["value"]
    return schemas.TotalDisplay(total=total)

@router.get("/{id}", response_model=schemas.ExpenseInResponse)
async def get_expense_by_id(id: schemas.PyObjectId):
    return crud.expenses_crud.get_by_id(id=id)

@router.put("/{id}", response_model=schemas.ExpenseInResponse)
async def update_Expense(
    id: schemas.PyObjectId,
    expense: schemas.ExpenseInUpdate,
    user: schemas.UserInResponse = Depends(get_current_user)
    ):
    if expense.value:
        existing_expense = schemas.ExpenseInResponse(**crud.expenses_crud.get_by_id(id=id))
        user_account = schemas.AccountInResponse(**crud.accounts_crud.get_by_user_id(
            user_id=user.id
        ))
        balance = user_account.balance
        new_balance = (balance + existing_expense.value) - expense.value
        crud.accounts_crud.update(
            id=user_account.id,
            obj_in=schemas.AccountInUpdate(balance=new_balance)
            )
    return crud.expenses_crud.update(id=id, obj_in=expense)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_Expense(
    id: schemas.PyObjectId,
    user: schemas.UserInResponse = Depends(get_current_user)
    ):
    existing_expense = schemas.ExpenseInResponse(**crud.expenses_crud.get_by_id(id=id))
    user_account = schemas.AccountInResponse(**crud.accounts_crud.get_by_user_id(
        user_id=user.id
    ))
    balance = user_account.balance
    new_balance = balance + existing_expense.value
    crud.accounts_crud.update(
        id=user_account.id,
        obj_in=schemas.AccountInUpdate(balance=new_balance)
        )
    return crud.expenses_crud.delete(id=id)
