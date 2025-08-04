from dto.base_dto import Base
from pydantic import Field
class TitlesDto(Base):
    name: str = Field(alias="title")