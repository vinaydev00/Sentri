from fastapi import APIRouter
from app.middleware.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/token")
def get_demo_token():
    """Demo endpoint — issues a JWT for testing. In prod, validate real credentials."""
    token = create_access_token({"sub": "demo-client", "role": "client"})
    return {"access_token": token, "token_type": "bearer"}