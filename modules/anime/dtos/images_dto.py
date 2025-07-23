from dto.base_dto import Base
from pydantic import HttpUrl


class ImagesDto(Base):
    small_image: HttpUrl
    large_image: HttpUrl
