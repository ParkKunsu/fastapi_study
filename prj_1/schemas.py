from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str  # 해시전 패스워드 입력 받음


class UserLogin(BaseModel):
    username: str
    password: str  # 해시전 패스워드 입력 받음


class MemoCreate(BaseModel):
    title: str
    content: str


class MemoUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
