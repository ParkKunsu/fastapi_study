# FastAPI Study

FastAPI 학습을 위한 프로젝트

## 기술 스택

- Python 3.12
- FastAPI
- SQLAlchemy (Async)
- Jinja2 (템플릿 엔진)
- MySQL + aiomysql
- bcrypt (비밀번호 암호화)

## 프로젝트 구조

```
fast_api/
├── prj_1/                  # 메모 앱 (MVC 패턴, 비동기)
│   ├── main.py             # FastAPI 앱 초기화, lifespan
│   ├── controllers.py      # 라우터 및 API 엔드포인트
│   ├── models.py           # SQLAlchemy ORM 모델
│   ├── schemas.py          # Pydantic 스키마
│   ├── database.py         # DB 엔진 및 세션 설정
│   ├── dependencies.py     # 의존성 (DB 세션, 비밀번호 해싱)
│   └── templates/          # Jinja2 HTML 템플릿
│       ├── home.html
│       └── memos.html
└── prj_2/                  # (예정)
```

## 주요 기능

- 회원가입 / 로그인 / 로그아웃 (세션 기반)
- 비밀번호 암호화 (bcrypt)
- 메모 CRUD (생성, 조회, 수정, 삭제)
- 유저별 메모 권한 관리 (본인 메모만 수정/삭제)

## 실행 방법

```bash
# 환경 활성화
conda activate fastapi

# 패키지 설치
pip install fastapi uvicorn sqlalchemy aiomysql bcrypt python-dotenv jinja2 python-multipart

# .env 파일 생성 (prj_1 디렉토리)
# ASYNC_DATABASE_URL=mysql+aiomysql://유저:비밀번호@호스트:포트/DB이름

# 실행
cd prj_1
uvicorn main:app --reload
```

## 커밋 히스토리

| 날짜 | 타입 | 내용 |
|------|------|------|
| 2026-04-04 | feat | 프로젝트 초기화 |
| 2026-04-05 | feat | 로그인 기능 구현 - 비밀번호 암호화, 세션 기능 추가 |
| 2026-04-05 | feat | 로그인 기능 구현 - 로그인, 로그아웃 구현 |
| 2026-04-12 | feat | 메모, 회원 DB 연동 - 메모 DB에 유저 ID FK 추가 |
| 2026-04-19 | feat | 메모 수정, 삭제 시 유저 ID 조회 및 비교 추가 |
| 2026-04-19 | feat | 프론트 개선 및 예외처리 추가 |
| 2026-04-19 | refactor | MVC 패턴 적용, DB 비동기 전환 |
