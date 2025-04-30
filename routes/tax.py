# app/routes/tax.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, models, database

tax_router = APIRouter()

@tax_router.get("/tax-records/{user_id}", response_model=list[models.TaxRecordOut])
def get_tax_records(user_id: int, db: Session = Depends(database.get_db)):
    # Fetch user tax records based on the user_id
    return crud.get_user_tax_records(db, user_id)


    ...
