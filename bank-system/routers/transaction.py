from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User, Transaction
from schemas import TransactionRequest, TransactionResponse, BalanceResponse
from utils import create_response

router = APIRouter(prefix="/api/transaction", tags=["Transactions"])

@router.post("/credit/{user_id}", response_model=dict)
def credit_amount(user_id: str, transaction: TransactionRequest, db: Session = Depends(get_db)):
    """
    Credit amount to user account
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if transaction.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount must be greater than 0"
        )
    
    # Update balance
    user.balance += transaction.amount
    
    # Create transaction record
    trans_record = Transaction(
        user_id=user.id,
        transaction_type="CREDIT",
        amount=transaction.amount,
        balance_after=user.balance,
        description=transaction.description or "Credit"
    )
    
    db.add(trans_record)
    db.commit()
    db.refresh(trans_record)
    
    return create_response(
        success=True,
        message="Credit successful!",
        data={
            "transaction_id": trans_record.id,
            "user_id": user.user_id,
            "amount": transaction.amount,
            "new_balance": user.balance,
            "description": trans_record.description,
            "timestamp": trans_record.created_at
        }
    )

@router.post("/debit/{user_id}", response_model=dict)
def debit_amount(user_id: str, transaction: TransactionRequest, db: Session = Depends(get_db)):
    """
    Debit amount from user account
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if transaction.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount must be greater than 0"
        )
    
    # Check sufficient balance
    if user.balance < transaction.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient balance. Current balance: {user.balance}"
        )
    
    # Update balance
    user.balance -= transaction.amount
    
    # Create transaction record
    trans_record = Transaction(
        user_id=user.id,
        transaction_type="DEBIT",
        amount=transaction.amount,
        balance_after=user.balance,
        description=transaction.description or "Debit"
    )
    
    db.add(trans_record)
    db.commit()
    db.refresh(trans_record)
    
    return create_response(
        success=True,
        message="Debit successful!",
        data={
            "transaction_id": trans_record.id,
            "user_id": user.user_id,
            "amount": transaction.amount,
            "new_balance": user.balance,
            "description": trans_record.description,
            "timestamp": trans_record.created_at
        }
    )

@router.get("/balance/{user_id}", response_model=dict)
def get_balance(user_id: str, db: Session = Depends(get_db)):
    """
    Get current balance of user
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return create_response(
        success=True,
        message="Balance retrieved successfully!",
        data={
            "user_id": user.user_id,
            "current_balance": user.balance,
            "account_status": "Active" if user.is_active else "Inactive"
        }
    )

@router.get("/history/{user_id}", response_model=dict)
def get_transaction_history(user_id: str, db: Session = Depends(get_db)):
    """
    Get transaction history for user
    """
    user = db.query(User).filter(User.user_id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    transactions = db.query(Transaction).filter(Transaction.user_id == user.id).all()
    
    trans_data = [
        {
            "id": t.id,
            "type": t.transaction_type,
            "amount": t.amount,
            "balance_after": t.balance_after,
            "description": t.description,
            "timestamp": t.created_at
        }
        for t in transactions
    ]
    
    return create_response(
        success=True,
        message="Transaction history retrieved successfully!",
        data={
            "user_id": user.user_id,
            "total_transactions": len(trans_data),
            "transactions": trans_data
        }
    )