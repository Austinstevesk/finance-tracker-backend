from fastapi import HTTPException, status
from app.crud.crud_base import CRUDBase
from app import schemas
from app.db.mongodb import user_collection
from app.utils.password_utils import hash, verify
from app.utils.oauth2 import access_security, refresh_security



user_crud = CRUDBase(user_collection, "User")
from app.crud.crud_accounts import accounts_crud

def create_user(user: schemas.UserInSignUp):
    existing_user = user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email address already exists"
        )
    user = schemas.ExtendedUserInSignup(**schemas.UserInDB(**user.__dict__).__dict__)
    # hash password
    user.password = hash(password=user.password)
    user = user_crud.create(obj_in=user)
    user_account = schemas.AccountCreate(
        user_id=user["_id"],
        balance=0.0,
    )
    accounts_crud.create(obj_in=user_account)
    return user

def login_user(user: schemas.UserInLogin):
    existing_user = user_collection.find_one({"email": user.email})
    if not existing_user or not verify(user.password, existing_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    # create token
    subject = {"id": str(existing_user["_id"])}
    access_token = access_security.create_access_token(subject=subject)
    refresh_token = refresh_security.create_refresh_token(subject=subject)
    return schemas.LoginData(
        access_token=access_token,
        refresh_token=refresh_token,
        user=existing_user
    )