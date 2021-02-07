import importlib.resources
import json

from flask import Flask, render_template, request
from flask_pydantic import validate

from models import QuizForm

app = Flask(__name__, static_url_path='')


@app.route('/answer', methods=('POST',))
@validate()
def submit_answer(body: QuizForm):
    request.is_multiprocess
    body.grade_name
    return 'Hello World!'


@app.route('/', methods=('GET',))
def index():
    with importlib.resources.open_text('resource', 'qna.json') as data_file:
        qnas = json.load(data_file)
    with importlib.resources.open_text('resource', 'grade_names.json') as data_file:
        grade_names = json.load(data_file)
    with importlib.resources.open_text('resource', 'cafe_names.json') as data_file:
        cafe_names = json.load(data_file)

    return render_template(
        'index.html',
        qnas=enumerate(qnas),
        offset=10,
        cafe_names=enumerate(cafe_names),
        grade_names=enumerate(grade_names),
    )
