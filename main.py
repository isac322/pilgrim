import http
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence, Tuple

import aiofiles
import ujson
from aiocache import cached
from ddtrace import patch_all
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from tortoise.contrib.fastapi import register_tortoise

import config
import form
import models

_settings = config.Settings()

GRADE_NAME_FILE_NAME = 'grade_names.json'
CAFE_NAME_FILE_NAME = 'cafe_names.json'
QUIZ_FILE_NAME = 'quiz.json'

app = FastAPI(title='Pilgrim', version='0.2.9', docs_url=None, redoc_url=None, openapi_url=None)
app.mount('/static', StaticFiles(directory='static'), name='static')
app.mount('/img', StaticFiles(directory=str(_settings.resource_path / _settings.image_path)), name='images')
_templates = Jinja2Templates(directory='templates')


if _settings.dd_on:
    patch_all()


@app.post('/answer')
async def submit_answer(body: form.QuizForm):
    grade_names = await _read_json_resource(_settings.resource_path / GRADE_NAME_FILE_NAME)
    cafe_names = await _read_json_resource(_settings.resource_path / CAFE_NAME_FILE_NAME)

    if validate_answer(body, cafe_names, grade_names):
        await models.Answer.create(
            name=body.name,
            grade_name=grade_names[body.grade_name],
            cafe_name=ujson.dumps(tuple(map(cafe_names.__getitem__, body.cafe_name))),
            feedback=body.feedback,
        )
        return Response(status_code=http.HTTPStatus.CREATED)
    else:
        return Response(status_code=http.HTTPStatus.BAD_REQUEST)


def validate_answer(body: form.QuizForm, cafe_names: Sequence[str], grade_names: Sequence[str]) -> bool:
    return all(map(lambda e: e < len(cafe_names), body.cafe_name)) and body.grade_name < len(grade_names)


@cached(ttl=30 * 60)  # 30min
async def _read_json_resource(file_path: Path) -> Any:
    async with aiofiles.open(file_path) as fp:
        return ujson.loads(await fp.read())


@cached()
async def _list_image_files(parent_path: Path) -> Tuple[str, ...]:
    return tuple(map(lambda p: p.name, parent_path.iterdir()))


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    qnas = await _read_json_resource(_settings.resource_path / 'qna.json')
    grade_names = await _read_json_resource(_settings.resource_path / GRADE_NAME_FILE_NAME)
    cafe_names = await _read_json_resource(_settings.resource_path / CAFE_NAME_FILE_NAME)
    quiz_dict = await _read_json_resource(_settings.resource_path / QUIZ_FILE_NAME)
    quiz_deadline = datetime.fromisoformat(quiz_dict['deadline'])
    interviewer_map = await _read_json_resource(_settings.resource_path / 'interviewer_map.json')
    image_path_list = map(
        lambda p: request.url_for('images', path=p),
        await _list_image_files(_settings.resource_path / _settings.image_path),
    )

    return _templates.TemplateResponse(
        'index.html',
        dict(
            request=request,
            qnas=qnas,
            interviewer_map=interviewer_map,
            offset=_settings.question_offset,
            cafe_names=cafe_names,
            grade_names=grade_names,
            image_names=tuple(image_path_list),
            is_quiz_available=datetime.now(timezone.utc) <= quiz_deadline,
            quiz_dict=quiz_dict,
            quiz_deadline=quiz_deadline,
        ),
    )


register_tortoise(
    app,
    db_url=_settings.db_url,
    modules=dict(models=['models']),
    generate_schemas=True,
    add_exception_handlers=True,
)
