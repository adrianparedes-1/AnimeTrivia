from pydantic import BaseModel, EmailStr
from typing import Dict

class PlayerProfileDTO(BaseModel):
    username: str
    display_name: str
    email: EmailStr
    player_history: Dict