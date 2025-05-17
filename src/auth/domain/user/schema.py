from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class UserOut(BaseModel):
    id: UUID
    email: str
    name: str

    class Config:
        from_attributes = True
