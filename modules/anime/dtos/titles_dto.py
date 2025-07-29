from dto.base_dto import Base
from pydantic import Field
class TitlesDto(Base):
    type: str
    name: str = Field(alias="title")