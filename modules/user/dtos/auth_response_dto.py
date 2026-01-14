from pydantic import BaseModel
from typing import Optional

class SpotifyLoginResponse(BaseModel):
    code: Optional[str] = None
    state: Optional[str] = None
