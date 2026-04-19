from database import AsyncSessionLocal
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 로그인을 위한 비밀번호 암호화
def get_password_hash(password):
    return pwd_context.hash(password)


# 비밀번호 검증
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# db 세션 생성
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
        await session.commit()
