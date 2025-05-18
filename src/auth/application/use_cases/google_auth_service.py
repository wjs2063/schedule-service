import time
from src.auth.infra.external_apis.google.google_oauth import exchange_code, get_user_info, refresh_access_token
from src.auth.infra.repository.rdb_repository.user_repository import UserRepository

class AuthService:
    @staticmethod
    async def login_with_google(code: str):
        token_data = await exchange_code(code)
        user_data = await get_user_info(token_data["access_token"])
        user_record = {
            "email": user_data["email"],
            "name": user_data["name"],
            "provider":"google",
            "provider_user_id": user_data["id"],
            "access_token": token_data["access_token"],
            "refresh_token": token_data.get("refresh_token"),
            "expires_at": time.time() + int(token_data["expires_in"])
        }
        return await UserRepository.save_user(user_record,provider="google")

    @staticmethod
    async def get_valid_token(user_id: str) -> str:
        user = await UserRepository.get_user(user_id)
        if not user:
            raise ValueError("User not found")

        if user.expires_at > time.time():
            return user.access_token

        refreshed = await refresh_access_token(user.refresh_token)
        await UserRepository.update_token(user, refreshed["access_token"], time.time() + int(refreshed["expires_in"]))
        return refreshed["access_token"]



    @staticmethod
    async def get_access_token_from_refresh_token(refresh_token: str) -> str:
        user = await UserRepository.get_user_by_refresh_token(refresh_token)
        if not user:
            raise ValueError("Invalid refresh token")

        if user.expires_at > time.time():
            return user.access_token

        refreshed = await refresh_access_token(refresh_token)
        await UserRepository.update_token(user, refreshed["access_token"], time.time() + int(refreshed["expires_in"]))
        return refreshed["access_token"]