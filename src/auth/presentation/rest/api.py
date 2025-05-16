from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/login")
async def login():
    return {"message": "Login successful"}


@auth_router.post("/logout")
async def logout():
    return {"message": "Logout successful"}


@auth_router.post("/user")
async def sign_up():
    return {"message": "Sign in successful"}


@auth_router.delete("/user/register")
async def delete_user():
    return {"message": "User deleted successfully"}

