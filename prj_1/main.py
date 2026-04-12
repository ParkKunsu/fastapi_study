import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

load_dotenv()


app = FastAPI()
# 세션을 위한 미들웨어 추가
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")
templates = Jinja2Templates(directory="templates")

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Base = declarative_base()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 로그인을 위한 비밀번호 암호화
def get_password_hash(password):
    return pwd_context.hash(password)


# 비밀번호 검증
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


########## 유저 디비 ##########
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(200))
    hashed_password = Column(String(512))


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str  # 해시전 패스워드 입력 받음


########################################


########## 메모 디비 ##########
class Memo(Base):
    __tablename__ = "memo"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(100))
    content = Column(String(1000))


class MemoCreate(BaseModel):
    title: str
    content: str


class MemoUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


########################################


# db 세션 생성
def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)


########## 가입, 로그인, 로그아웃 ##########
@app.post("/signup")
async def signup(signup_data: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(signup_data.password)
    new_user = User(username=signup_data.username, email=signup_data.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Account created successfully", "user_id": new_user.id}


# 로그인
@app.post("/login")
async def login(request: Request, signin_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == signin_data.username).first()
    if user and verify_password(signin_data.password, user.hashed_password):
        request.session["username"] = user.username
        return {"message": "Logged in successfully"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


# 로그아웃
@app.post("/logout")
async def logout(request: Request):
    request.session.pop("username", None)
    return {"message": "Logged out successfully"}


########################################


########## 메모 CRUD ##########
# 메모 생성
@app.post("/memos/")
async def create_memo(request: Request, memo: MemoCreate, db: Session = Depends(get_db)):
    username = request.session.get("username")
    if username is None:
        raise HTTPException(status_code=401, detail="Not authorized")
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    new_memo = Memo(user_id=user.id, title=memo.title, content=memo.content)
    db.add(new_memo)
    db.commit()
    db.refresh(new_memo)
    return new_memo


# 메모 조회
@app.get("/memos/")
async def list_memos(request: Request, db: Session = Depends(get_db)):
    username = request.session.get("username")
    if username is None:
        raise HTTPException(status_code=401, detail="Not authorized")
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    memos = db.query(Memo).filter(Memo.user_id == user.id).all()
    return templates.TemplateResponse(request=request, name="memos.html", context={"memos": memos})


# 메모 수정
@app.put("/memos/{memo_id}")
async def update_memo(memo_id: int, memo: MemoUpdate, db: Session = Depends(get_db)):
    db_memo = db.query(Memo).filter(Memo.id == memo_id).first()
    if db_memo is None:
        return {"error": "Memo not found"}

    if memo.title is not None:
        db_memo.title = memo.title
    if memo.content is not None:
        db_memo.content = memo.content

    db.commit()
    db.refresh(db_memo)
    return {"id": db_memo.id, "title": db_memo.title, "content": db_memo.content}


# 메모 삭제
@app.delete("/memos/{memo_id}")
async def delete_memo(memo_id: int, db: Session = Depends(get_db)):
    db_memo = db.query(Memo).filter(Memo.id == memo_id).first()
    if db_memo is None:
        return {"error": "Memo not found"}

    db.delete(db_memo)
    db.commit()
    return {"message": "Memo is deleted"}


########################################


# 기본 라우트
@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse(name="home.html", request=request)


@app.get("/about")
async def about():
    return {"message": "이것은 마이 메모 앱의 소개 페이지입니다."}
