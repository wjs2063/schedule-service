import os
## auth/presentation/router.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from src.auth.application.use_cases.google_auth_service import AuthService
from src.auth.domain.user.schema import UserOut
from src.auth.infra.external_apis.google.google_oauth import get_auth_url

auth_router = APIRouter()

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/auth/callback"

SCOPE = "openid email profile https://www.googleapis.com/auth/calendar.readonly"


@auth_router.get("/login")
def login():
    return RedirectResponse(get_auth_url())

@auth_router.get("/auth/callback", response_model=UserOut)
async def callback(code: str):
    try:
        print("/auth/callback")
        user = await AuthService.login_with_google(code)
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@auth_router.post("/logout")
async def logout():
    return {"message": "Logout successful"}


@auth_router.post("/user")
async def sign_up():
    return {"message": "Sign in successful"}


@auth_router.delete("/user/register")
async def delete_user():
    return {"message": "User deleted successfully"}

