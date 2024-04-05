from fastapi import APIRouter, Depends, HTTPException, status
from .... import schemas, crud
from ....utils.oauth2 import get_current_user

router = APIRouter(
    prefix="/budgets", tags=["Budgets"],
    dependencies=[Depends(get_current_user)]
    )

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.BudgetInResponse)
async def create_user_budget(
    budget: schemas.BudgetCreate,
    user: schemas.UserInResponse = Depends(get_current_user)
):
    user_budget = schemas.ExtendedBudgetCreate(
        **budget.__dict__,
        user_id=user.id,
    )
    return crud.budgets_crud.create(obj_in=user_budget)

@router.get("/{id}", response_model=schemas.BudgetInResponse)
async def get_budget_by_id(id: schemas.PyObjectId):
    return crud.budgets_crud.get_by_id(id=id)

@router.put("/{id}", response_model=schemas.BudgetInResponse)
async def update_budget(id: schemas.PyObjectId, budget: schemas.BudgetInUpdate):
    return crud.budgets_crud.update(id=id, obj_in=budget)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_budget(id: schemas.PyObjectId):
    return crud.budgets_crud.delete(id=id)
