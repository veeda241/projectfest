from fastapi import FastAPI
from app.routes import registration_router, login_router, bank_router, tax_router

app = FastAPI(
    title="Robinhood Taxation API",
    description="Backend service for user registration, bank linking, and tax verification",
    version="1.0.0"
)

# Include routers
app.include_router(registration_router, prefix="/auth", tags=["Authentication"])
app.include_router(login_router, prefix="/auth", tags=["Authentication"])
app.include_router(bank_router, prefix="/bank", tags=["Bank Account"])
app.include_router(tax_router, prefix="/tax", tags=["Tax"])

# Root path
@app.get("/")
def read_root():
    return {"message": "Welcome to the Robinhood Taxation API"}

