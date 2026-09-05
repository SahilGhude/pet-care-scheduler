from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.user_model import User
from app.schemas.user_schema import (
    UserCreate,
    UserResponse,
    UserUpdate,
    UserLogin,
    ResetPassword
)
import asyncio
import random
from app.utils.otp_store import otp_storage
from app.utils.email_service import send_email
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
    full_name=user.full_name,
    email=user.email,
    phone=user.phone,
    password=user.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login")
def login_user(
    login: UserLogin,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == login.email
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid Email"
        )

    if user.password != login.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid Password"
        )
    return {
    "message": "Login Successful",
    "user_id": user.id,
    "full_name": user.full_name,
    "email": user.email
    }

@router.get("/", response_model=list[UserResponse])
def get_all_user(
    db: Session = Depends(get_db)
):

    users = db.query(User).all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_by_id(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    updated_user: UserUpdate,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.full_name = updated_user.full_name
    user.email = updated_user.email
    user.phone = updated_user.phone
    user.password = updated_user.password
    db.commit()
    db.refresh(user)

    return user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="No user found"
        )

    db.delete(user)
    db.commit()

    return {
        "message": "User deleted successfully"
    }
@router.post("/forgot-password")
def forgot_password(
    email: str,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Email not found"
        )

    otp = str(
        random.randint(100000, 999999)
    )

    otp_storage[email] = otp

    

    asyncio.run(
        send_email(
        email=email,
        subject="Pet Care Scheduler Password Reset",
        body=f"""
Hello,

Your OTP for password reset is:

{otp}

Do not share this OTP with anyone.

Pet Care Scheduler Team
"""
    )
    )

    return {
        "message": "OTP Sent"
    }
@router.post("/verify-otp")
def verify_otp(
    email: str,
    otp: str
):

    if otp_storage.get(email) != otp:
        raise HTTPException(
            status_code=400,
            detail="Invalid OTP"
        )

    return {
        "message": "OTP Verified"
    }
@router.post("/reset-password")
def reset_password(
    data: ResetPassword,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.password = data.new_password

    db.commit()
    db.refresh(user)

    return {
        "message": "Password Updated"
    }