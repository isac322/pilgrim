import importlib.resources
import json

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from models import QuizForm

app = FastAPI(title='Pilgrim', docs_url=None, redoc_url=None)
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')


@app.post('/answer')
async def submit_answer(body: QuizForm):
    return 'Hello World!'


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    with importlib.resources.open_text('resource', 'qna.json') as data_file:
        qnas = json.load(data_file)
    with importlib.resources.open_text('resource', 'grade_names.json') as data_file:
        grade_names = json.load(data_file)
    with importlib.resources.open_text('resource', 'cafe_names.json') as data_file:
        cafe_names = json.load(data_file)

    return templates.TemplateResponse(
        'index.html',
        dict(
            request=request,
            qnas=enumerate(qnas),
            offset=10,
            cafe_names=enumerate(cafe_names),
            grade_names=enumerate(grade_names),
        ),
    )
