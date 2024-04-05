from fastapi import APIRouter, Depends, status
from typing import List
from app import schemas, crud
from app.utils.oauth2 import get_current_user

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

@router.get("/user-budgets", response_model=List[schemas.BudgetInResponse])
async def get_user_budgets(user: schemas.UserInResponse = Depends(get_current_user)):
    return crud.budgets_crud.get_many_by_user_id(user_id=user.id)

@router.get("/user-expenses", response_model=List[schemas.ExpenseInResponse])
async def get_user_expenses(user: schemas.UserInResponse = Depends(get_current_user)):
    return crud.expenses_crud.get_many_by_user_id(user_id=user.id)

@router.get("/user-goals", response_model=List[schemas.GoalInResponse])
async def get_user_goals(user: schemas.UserInResponse = Depends(get_current_user)):
    return crud.goals_crud.get_many_by_user_id(user_id=user.id)

@router.get("/user-incomes", response_model=List[schemas.IncomeInResponse])
async def get_user_incomes(user: schemas.UserInResponse = Depends(get_current_user)):
    return crud.income_crud.get_many_by_user_id(user_id=user.id)

@router.get("/user-liabilities", response_model=List[schemas.LiabilityInResponse])
async def get_user_liabilities(user: schemas.UserInResponse = Depends(get_current_user)):
    return crud.liabilities_crud.get_many_by_user_id(user_id=user.id)

@router.get("/{id}", response_model=schemas.UserInResponse)
async def get_user_by_id(id: schemas.PyObjectId):
    return crud.user_crud.get_by_id(id=id)

@router.put("/{id}", response_model=schemas.UserInResponse)
async def update_user(id: schemas.PyObjectId, user: schemas.UserInUpdate):
    return crud.user_crud.update(id=id, obj_in=user)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: schemas.PyObjectId):
    return crud.user_crud.delete(id=id)