from pydantic import BaseModel
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    phone :str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    full_name: str
    email: str
    phone: str
    password: str

class ResetPassword(BaseModel):
    email: EmailStr
    new_password: str