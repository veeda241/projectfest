# app/routes/registration.py
from app.models import UserCreate, UserOut
from app.db_models import User  # if needed

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app import db_models, database, models

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=models.UserOut)
def register_user(user: models.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(db_models.User).filter(db_models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(user.password)
    new_user = db_models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        pan=user.pan,
        income=user.income
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, crud

router = APIRouter()

@router.post("/register", response_model=models.UserOut)
def register_user(user: models.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

# ✅ Export the router
registration_router = router
# app/routes/registration.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, models, database

registration_router = APIRouter()

@registration_router.post("/register", response_model=models.UserOut)
def register_user(user: models.UserCreate, db: Session = Depends(database.get_db)):
    return crud.create_user(db=db, user=user)

