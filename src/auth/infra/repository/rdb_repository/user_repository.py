from src.auth.domain.user.model import User
from typing import Optional, Literal
import time


class UserRepository:
    @staticmethod
    async def save_user(user_data: dict, provider: Literal["google", "kakao", "naver"]):
        # TODO : User token 필터링 로직

        user = await User.filter(provider=provider, email=user_data["email"]).first()
        if user:
            await user.delete()

        return await User.create(**user_data)

    @staticmethod
    async def get_user(user_id: str) -> Optional[User]:
        return await User.get_or_none(id=user_id)

    @staticmethod
    async def update_token(user: User, access_token: str, expires_at: float):
        user.access_token = access_token
        user.expires_at = expires_at
        await user.save()

    @staticmethod
    async def get_user_by_refresh_token(refresh_token: str) -> Optional[User]:
        return await User.get_or_none(refresh_token=refresh_token)