import re
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime, timedelta
from .base import DateMixins, PyObjectId

class UserInDB(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    
class UserInSignUp(UserInDB):
    confirm_password: str
    
    class Config:
        schema_extra = {
            "example": {
                "full_name": "example fullname",
                "email": "user@example.com",
                "password": "Fake@Password1",
                "confirm_password": "Fake@Password1",
            }
        }

    # validate password is a combination of strings, nums and special chars
    @validator("password")
    def password_is_valid(cls, password: Optional[str]) -> Optional[str]:
        regex = re.compile("[@_!#$%^&*()<>?/\|}{~:.-]")
        if len(password) < 8:
            raise ValueError("Passwords must be at least 8 characters")
        elif re.search("[0-9]", password) is None:
            raise ValueError("Passwords must contain at least 1 number")
        elif re.search("[A-Z]", password) is None:
            raise ValueError("Passwords must contain at least 1 uppercase letter")
        elif re.search("[a-z]", password) is None:
            raise ValueError("Passwords must contain at least 1 lowercase letter")
        elif regex.search(password) is None:
            raise ValueError("Passwords must contain at least 1 special character")
        else:
            return password

class ExtendedUserInSignup(UserInDB, DateMixins):
    pass

class UserInResponse(DateMixins):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    full_name: str
    email: EmailStr


class UserInLogin(BaseModel):
    email: EmailStr
    password: str

def get_expire_timestamp():
    return datetime.utcnow() + timedelta(days=7)

class LoginData(BaseModel):
    access_token: str
    refresh_token: str
    token_type: Optional[str] = "bearer"
    expire: Optional[datetime] = get_expire_timestamp()
    user: UserInResponse

class UserInUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
