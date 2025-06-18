from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserResponseDTO(BaseModel):
    username: str = Field(alias='id')
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    display_name: str
    provider: str