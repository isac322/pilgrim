import http
import importlib.resources
import json
from pathlib import Path
from typing import Sequence

import aiofiles
from aiocache import cached
from ddtrace import patch_all
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import FileResponse, HTMLResponse, Response
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from tortoise.contrib.fastapi import register_tortoise

import config
import form
import models

app = FastAPI(title='Pilgrim', version='0.2.8', docs_url=None, redoc_url=None, openapi_url=None)
app.mount('/static', StaticFiles(directory='static'), name='static')
_templates = Jinja2Templates(directory='templates')

_settings = config.Settings()

if _settings.dd_on:
    patch_all()


@app.post('/answer')
async def submit_answer(body: form.QuizForm):
    grade_names = await _read_json_resource(_settings.grade_names_file_path)
    cafe_names = await _read_json_resource(_settings.cafe_names_file_path)

    if validate_answer(body, cafe_names, grade_names):
        await models.Answer.create(
            name=body.name,
            grade_name=grade_names[body.grade_name],
            cafe_name=json.dumps(tuple(map(cafe_names.__getitem__, body.cafe_name))),
            feedback=body.feedback,
        )
        return Response(status_code=http.HTTPStatus.CREATED)
    else:
        return Response(status_code=http.HTTPStatus.BAD_REQUEST)


def validate_answer(body: form.QuizForm, cafe_names: Sequence[str], grade_names: Sequence[str]) -> bool:
    return all(map(lambda e: e < len(cafe_names), body.cafe_name)) and body.grade_name < len(grade_names)


@cached()
async def _read_json_resource(file_path: Path) -> str:
    async with aiofiles.open(file_path) as fp:
        return json.loads(await fp.read())


image_path = importlib.resources.files('resource.images')
image_map = {str(path.relative_to(image_path)): path for path in image_path.glob('*.jpg')}


@app.get('/img/{image_name}', name='images')
async def image(request: Request, image_name: str):
    if image_name not in image_map:
        return Response(status_code=http.HTTPStatus.NOT_FOUND)

    return FileResponse(image_map[image_name])


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    qnas = await _read_json_resource(_settings.qna_file_path)
    grade_names = await _read_json_resource(_settings.grade_names_file_path)
    cafe_names = await _read_json_resource(_settings.cafe_names_file_path)
    image_path_list = map(lambda i: request.url_for('images', image_name=i), image_map.keys())

    return _templates.TemplateResponse(
        'index.html',
        dict(
            request=request,
            qnas=enumerate(qnas),
            offset=10,
            cafe_names=enumerate(cafe_names),
            grade_names=enumerate(grade_names),
            image_names=tuple(enumerate(image_path_list)),
        ),
    )


register_tortoise(
    app,
    db_url=_settings.db_url,
    modules=dict(models=['models']),
    generate_schemas=True,
    add_exception_handlers=True,
)
