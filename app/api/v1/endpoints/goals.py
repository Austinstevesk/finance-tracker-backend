from fastapi import APIRouter, Depends, HTTPException, status
from .... import schemas, crud
from ....utils.oauth2 import get_current_user

router = APIRouter(
    prefix="/goals", tags=["Goals"],
    dependencies=[Depends(get_current_user)]
    )

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.GoalInResponse)
async def create_user_goal(
    goal: schemas.GoalCreate,
    user: schemas.UserInResponse = Depends(get_current_user)
):
    user_goal = schemas.ExtendedGoalCreate(
        **goal.__dict__,
        user_id=user.id,
    )
    return crud.goals_crud.create(obj_in=user_goal)

@router.get("/{id}", response_model=schemas.GoalInResponse)
async def get_goal_by_id(id: schemas.PyObjectId):
    return crud.goals_crud.get_by_id(id=id)

@router.put("/{id}", response_model=schemas.GoalInResponse)
async def update_goal(id: schemas.PyObjectId, goal: schemas.GoalInUpdate):
    return crud.goals_crud.update(id=id, obj_in=goal)

@router.put("/{id}/settle", response_model=schemas.GoalInResponse)
async def settle_goal(
    id: schemas.PyObjectId,
    user: schemas.UserInResponse = Depends(get_current_user),
    ):
    existing_goal = schemas.GoalInResponse(**crud.goals_crud.get_by_id(id=id))
    # update account balance
    user_account = schemas.AccountInResponse(**crud.accounts_crud.get_by_user_id(
        user_id=user.id
    ))
    balance = user_account.balance
    if existing_goal.closing_value > balance:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Your balance is too low to settle this goal"
        )
    new_balance = balance - existing_goal.closing_value
    crud.goals_crud.update(
        id=user_account.id,
        obj_in=schemas.AccountInUpdate(balance=new_balance)
        )
    return crud.goals_crud.update(
        id=id,
        obj_in=schemas.GoalInUpdate(is_settled=True)
        )

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal(id: schemas.PyObjectId):
    return crud.goals_crud.delete(id=id)