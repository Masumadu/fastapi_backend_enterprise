import uuid

from pydantic import BaseModel


class SampleSchema(BaseModel):
    title: str
    content: str

    class Config:
        orm_mode = True


class SampleOutSchema(SampleSchema):
    id: uuid.UUID
    content: str = None


class TokenSchema(BaseModel):
    access_token: str


class AuthSchema(BaseModel):
    user_id: str
