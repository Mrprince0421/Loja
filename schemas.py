# loja/schemas.py
from pydantic import BaseModel, EmailStr, ConfigDict
from pydantic.fields import Field

class Message(BaseModel):
    message: str

class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

class UserList(BaseModel):
    users: list[UserPublic]

class Token(BaseModel):
    access_token: str
    token_type: str

class ProductSchema(BaseModel):
    name: str
    description: str | None = None
    price: float
    QT: int # <- Corrigido aqui

class ProductPublic(BaseModel):
    id: int
    name: str
    price: float
    QT: int # <- Corrigido aqui
    model_config = ConfigDict(from_attributes=True)

class ProductUpdateSchema(BaseModel):
    name: str | None = Field(None)
    description: str | None = Field(None)
    price: float | None = Field(None)
    QT: int | None = Field(None) # <- Corrigido aqui