from sqlalchemy import Column, ForeignKey, Integer, String

from fast_api.prj_1.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(200))
    hashed_password = Column(String(512))


class Memo(Base):
    __tablename__ = "memo"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(100))
    content = Column(String(1000))
    content = Column(String(1000))
