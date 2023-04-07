import uuid

from pydantic import BaseModel


class SampleSchema(BaseModel):
    title: str
    content: str

    class Config:
        orm_mode = True


class SampleOutSchema(SampleSchema):
    id: uuid.UUID


class UpdateSampleSchema(BaseModel):
    title: str = None
    content: str = None


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class AuthSchema(BaseModel):
    user_id: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str
