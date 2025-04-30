from sqlalchemy.orm import Session
from app import db_models
from app.schemas import UserCreate, BankAccountCreate, UserLogin
from app.auth import hash_password, verify_password

from app import models

def create_user(db: Session, user: models.UserCreate):

    hashed_password = hash_password(user.password)
    db_user = db_models.User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # ← this gives you the real id from DB
    return db_user



# --- Verify user login ---
def verify_user_login(db: Session, user_login: UserLogin):
    db_user = db.query(db_models.User).filter(db_models.User.email == user_login.email).first()
    if db_user is None or not verify_password(user_login.password, db_user.password):
        raise Exception("Invalid credentials")
    return db_user


# --- Get user by email ---
def get_user_by_email(db: Session, email: str):
    return db.query(db_models.User).filter(db_models.User.email == email).first()


# --- Create a bank account and link to a user ---
def create_bank_account(db: Session, account: BankAccountCreate, user_id: int):
    db_account = db_models.BankAccount(
        account_number=account.account_number,
        bank_name=account.bank_name,
        account_type=account.account_type,
        balance=account.balance,
        user_id=user_id
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


# --- Tax calculation ---
def calculate_tax(income: float) -> float:
    """Calculate tax based on income"""
    if income > 500000:
        return income * 0.1  # 10% tax rate
    return 0.0  # No tax if income is less than ₹5,00,000


# --- Tax verification ---
def check_tax_paid_correctly(db: Session, user_id: int, bank_balance: float) -> bool:
    """Check if tax has been paid correctly"""
    expected_tax = calculate_tax(bank_balance)
    tax_record = db.query(db_models.TaxRecord).filter(db_models.TaxRecord.user_id == user_id).first()

    if tax_record:
        return tax_record.tax_paid == expected_tax
    return False  # If no tax record, tax is not paid correctly


# --- Record tax payment ---
def record_tax_payment(db: Session, user_id: int, amount: float):
    """Record the tax payment for a user"""
    tax_record = db_models.TaxRecord(user_id=user_id, tax_paid=amount)
    db.add(tax_record)
    db.commit()
    db.refresh(tax_record)
    return tax_record

def get_user_by_id(db: Session, user_id: int):
    return db.query(db_models.User).filter(db_models.User.id == user_id).first()
