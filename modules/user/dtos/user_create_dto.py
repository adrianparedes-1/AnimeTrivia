from pydantic import BaseModel, EmailStr, Field

class IgnoreExtraBase(BaseModel):
    model_config = {"extra": "ignore"}


class UserCreateDTO(IgnoreExtraBase):
    username: str = Field(alias='id')
    email: EmailStr
    display_name: str
