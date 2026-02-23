from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    user_id: str
    password: str
    name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    user_id: str
    name: str
    email: str
    phone: Optional[str]
    address: Optional[str]
    balance: float
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    user_id: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    message: str

class TransactionRequest(BaseModel):
    amount: float
    description: Optional[str] = None

class TransactionResponse(BaseModel):
    id: int
    user_id: int
    transaction_type: str
    amount: float
    balance_after: float
    description: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class BalanceResponse(BaseModel):
    user_id: str
    current_balance: float
    message: str