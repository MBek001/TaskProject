import datetime
import secrets

from pydantic import BaseModel


class UserRegistration(BaseModel):
    email: str
    name: str
    password1: str
    password2: str


class UserDatabase(BaseModel):
    email: str
    name: str
    password: str


class LoginUser(BaseModel):
    email: str
    password: str


class AllUserInfo(BaseModel):
    id: int
    name: str
    email: str
    is_admin: bool

class UserInfo(BaseModel):
    id: int
    name: str
    email: str
    joined_at: datetime.datetime
    user_photos: str
