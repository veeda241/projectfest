from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, database

# Create an instance of APIRouter for the tax routes
tax_router = APIRouter()

# Define the route for checking the tax status
@tax_router.get("/tax-status")
def get_tax_status(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get the bank account linked to this user
    bank_account = db.query(models.BankAccount).filter(models.BankAccount.user_id == user.id).first()
    if not bank_account:
        raise HTTPException(status_code=404, detail="Bank account not found")

    # Check if tax is paid correctly based on bank balance
    is_tax_paid = crud.check_tax_paid_correctly(db, user_id, bank_account.balance)
    return {"user_id": user.id, "is_tax_paid": is_tax_paid}

# app/routes.py
from fastapi import APIRouter

registration_router = APIRouter()

@registration_router.post("/register")
def register_user():
    # Add your registration logic here
    pass

from fastapi import APIRouter

registration_router = APIRouter()

@registration_router.post("/register")
def register_user():
    return {"message": "User registered"}
