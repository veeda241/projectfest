from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, crud

router = APIRouter()

@router.post("/login")
def login_user(user: models.UserLogin, db: Session = Depends(get_db)):
    return crud.login_user(db=db, user=user)

# ✅ Ensure that login_router is correctly exported
login_router = router
