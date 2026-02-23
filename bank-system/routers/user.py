from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from database import get_db
from models import User
from schemas import UserCreate, UserResponse, UserUpdate, LoginRequest, TokenResponse
from auth import hash_password, verify_password, create_access_token
from utils import create_response

router = APIRouter(prefix="/api/user", tags=["User Management"])

@router.post("/register", response_model=dict)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    # Check if user_id already exists
    existing_user = db.query(User).filter(User.user_id == user.user_id).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID already exists"
        )
    
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = hash_password(user.password)
    db_user = User(
        user_id=user.user_id,
        password=hashed_password,
        name=user.name,
        email=user.email,
        phone=user.phone,
        address=user.address,
        balance=0.0
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return create_response(
        success=True,
        message="User registered successfully!",
        data={"user_id": db_user.user_id, "name": db_user.name},
        status_code=201
    )

@router.post("/login", response_model=dict)
def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Login user and get access token
    """
    user = db.query(User).filter(User.user_id == login_data.user_id).first()
    
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.user_id},
        expires_delta=access_token_expires
    )
    
    return create_response(
        success=True,
        message="Login successful!",
        data={
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.user_id,
            "name": user.name
        }
    )

@router.get("/profile", response_model=dict)
def get_profile(user_id: str, db: Session = Depends(get_db)):
    """
    Get user profile
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user_data = {
        "id": user.id,
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "address": user.address,
        "balance": user.balance,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }
    
    return create_response(
        success=True,
        message="Profile retrieved successfully!",
        data=user_data
    )

@router.put("/profile/{user_id}", response_model=dict)
def update_profile(user_id: str, update_data: UserUpdate, db: Session = Depends(get_db)):
    """
    Update user profile
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update fields
    if update_data.name:
        user.name = update_data.name
    if update_data.email:
        # Check if new email is already used
        existing_email = db.query(User).filter(
            User.email == update_data.email,
            User.id != user.id
        ).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
        user.email = update_data.email
    if update_data.phone:
        user.phone = update_data.phone
    if update_data.address:
        user.address = update_data.address
    
    db.commit()
    db.refresh(user)
    
    return create_response(
        success=True,
        message="Profile updated successfully!",
        data={
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "address": user.address
        }
    )

@router.delete("/profile/{user_id}", response_model=dict)
def delete_profile(user_id: str, db: Session = Depends(get_db)):
    """
    Delete user profile (soft delete - deactivate)
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Soft delete - deactivate user
    user.is_active = False
    db.commit()
    
    return create_response(
        success=True,
        message="Profile deleted successfully!",
        data={"user_id": user.user_id}
    )