from pydantic import BaseModel, EmailStr
from typing import Optional

class UserResponseDTO(BaseModel):
    id: str | int
    email: EmailStr
    first_name: Optional[str]
    last_name: Optional[str]
    display_name: str
    provider: str