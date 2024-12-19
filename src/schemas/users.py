from pydantic import BaseModel


class UserRequestAdd(BaseModel):
    email: str
    password: str


class UsersAdd(BaseModel):
    email: str
    hashed_password: str


class User(BaseModel):
    id: int
    email: str
