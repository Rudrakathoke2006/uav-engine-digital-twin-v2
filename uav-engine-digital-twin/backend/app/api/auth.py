"""
Auth Router: Operator authentication.
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Auth"])

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(req: LoginRequest):
    return {
        "access_token": "defence-prototype-jwt-token",
        "token_type": "bearer",
        "operator_id": req.username,
        "role": "DEFENCE_OPERATOR"
    }
