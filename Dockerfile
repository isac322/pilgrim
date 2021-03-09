FROM python:3.9 AS dep

RUN pip install --no-cache-dir poetry
COPY poetry.lock pyproject.toml ./
RUN poetry export -f requirements.txt -o /tmp/requirements.txt

FROM isac322/uvicorn:py3.9-performance

MAINTAINER 'Byeonghoon Isac Yoo <bh322yoo@gmail.com>'

COPY --from=dep /tmp/requirements.txt /tmp/requirements.txt
RUN apk add --update --no-cache --virtual .build-deps g++ \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && apk --purge del .build-deps
COPY . /pilgrim/
WORKDIR /pilgrim
CMD ["main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers", "--forwarded-allow-ips", "*"]
