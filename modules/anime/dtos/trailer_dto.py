from dto.base_dto import Base
from pydantic import HttpUrl

class TrailerDto(Base):
    youtube_id: str
    url: HttpUrl
    embed_url: HttpUrl