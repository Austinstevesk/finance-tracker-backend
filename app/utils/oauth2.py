from datetime import timedelta
from app.db.mongodb import user_collection
from app.schemas import UserInResponse, PyObjectId
from app.core.settings.config import settings

from fastapi import HTTPException, Security, status
from fastapi_jwt import JwtAccessBearer, JwtAuthorizationCredentials, JwtRefreshBearer

access_security = JwtAccessBearer(
    secret_key=settings.ACCESS_TOKEN_SECRET_KEY,
    access_expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
)

refresh_security = JwtRefreshBearer(
    secret_key=settings.REFRESH_TOKEN_SECRET_KEY, access_expires_delta=timedelta(days=30)
)


def get_current_user(
    credentials: JwtAuthorizationCredentials = Security(access_security),
) -> UserInResponse:
    if not credentials:
        raise HTTPException(
            detail="Token provided is invalid",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    user = user_collection.find_one({"_id": PyObjectId(credentials.subject["id"])})
    if not user:
        raise HTTPException(
            detail="Token provided is invalid",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    return UserInResponse(**user)


def refresh_tokens(credentials: JwtAuthorizationCredentials = Security(refresh_security)
):
    # Update access/refresh tokens pair
    # We can customize expires_delta when creating
    access_token = access_security.create_access_token(subject=credentials.subject)
    refresh_token = refresh_security.create_refresh_token(subject=credentials.subject, expires_delta=timedelta(days=30))

    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}