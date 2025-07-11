from pydantic import BaseModel, EmailStr
from typing import Dict

class PlayerProfileDTO(BaseModel):
    id: int
    username: str
    display_name: str
    email: EmailStr
    player_history: Dict