from pydantic import BaseModel, EmailStr, Field

class IgnoreExtraBase(BaseModel):
    model_config = {"extra": "ignore"}


class OpenIDDTO(IgnoreExtraBase):
    username: str
    email: EmailStr
    display_name: str
