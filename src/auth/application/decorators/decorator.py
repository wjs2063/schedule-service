from functools import wraps
from fastapi import Request, HTTPException
from src.auth.application.use_cases.google_auth_service import AuthService

def ensure_fresh_access_token(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException(status_code=401, detail="Missing refresh token")

        try:
            access_token = await AuthService.get_access_token_from_refresh_token(refresh_token)
            request.state.access_token = access_token
            return await func(request, *args, **kwargs)
        except Exception as e:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

    return wrapper
