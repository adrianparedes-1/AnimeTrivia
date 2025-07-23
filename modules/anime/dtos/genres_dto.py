from dto.base_dto import Base
from pydantic import Field

class GenresDto(Base):
    genre: str = Field(alias="name")