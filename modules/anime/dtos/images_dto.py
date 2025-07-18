from dto.base_dto import Base
from pydantic import HttpUrl


class Images(Base):
    small_image: HttpUrl
    large_image: HttpUrl
