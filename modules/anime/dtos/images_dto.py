from dto.base_dto import Base
from pydantic import HttpUrl


class ImageContentDto(Base):
    small_image_url: HttpUrl
    large_image_url: HttpUrl

class ImagesDto(Base):
    jpg: ImageContentDto