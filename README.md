## Stack

- 언어: Python
- DB: SQLite3
- 패키지 매니저: [Poetry](https://python-poetry.org/)
- 웹서버 프레임워크: [FastAPI](https://fastapi.tiangolo.com/ko/) (ASGI)
- ORM: [Tortoise ORM](https://tortoise-orm.readthedocs.io/en/latest/)
- 프론트 프레임워크: [Bootstrap 5](https://getbootstrap.com/)

## 준비물

- Python 3.9
- \[필요한 경우\] Docker, Docker Compose
- 리소스 파일
  - 사진 파일
  - QnA 파일
  - 학년 이름 파일
  - 퀴즈 카페 이름 파일

## dependency 설치

#### Poetry 설치

https://python-poetry.org/docs/#installation 참고

터미널에서 `poetry install` 실행

## 서버 실행

### 환경 변수

`config.py`에 모든 필요한 변수들이 적혀있음

#### `PILGRIM_DB_URL`

DB에 쓰일 URL. 기본값으로는 현재 디렉토리에 `db.sqlite3` 파일 생성

#### `PILGRIM_RESOURCE_PATH`

이미지와 다른 파일들이 담겨있는 디렉토리 경로.

기본값으로는 현재 디렉토리의 `resource`를 사용한다.

##### 예시

```
resource
├── cafe_names.json
├── grade_names.json
├── images
│   ├── image1.jpg
│   └── image2.png
└── qna.json
```

#### `PILGRIM_IMAGE_PATH`

페이지 하단에 보여줄 이미지를 포함하고있는 디렉토리 이름.
`PILGRIM_RESOURCE_PATH` 와 조합해서 사용한다.

#### `PILGRIM_QUESTION_OFFSET`

질문 번호의 시작값.

#### `PILGRIM_DD_ON`

datadog 연동 파라미터.

### 실행

터미널에서 `PILGRIM_RESOURCE_PATH=resource_sample uvicorn main:app` 실행

`uvicorn main:app` 앞에 앞에서 설명한 environment 값들을 붙여서 설정 가능.

### Docker

`docker-compose up` 실행