from dto.base_dto import Base
from pydantic import HttpUrl
from typing import Optional
class TrailerDto(Base):
    youtube_id: Optional[str]
    url: Optional[HttpUrl]
    embed_url: Optional[HttpUrl]