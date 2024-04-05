from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from .... import schemas
from ....crud import crud_users

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserInResponse)
async def register_user(user: schemas.UserInSignUp):
    return crud_users.create_user(user=user)


@router.post("/login", response_model=schemas.LoginData)
async def login_user(user: schemas.UserInLogin):
    return crud_users.login_user(user=user)