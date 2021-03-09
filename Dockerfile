FROM python:3.9-slim AS dep

RUN apt-get update && apt-get install gcc libffi-dev cargo -y
RUN pip install --no-cache-dir poetry
COPY poetry.lock pyproject.toml ./
RUN poetry export -f requirements.txt -o /tmp/requirements.txt

FROM isac322/uvicorn:py3.9-performance

COPY --from=dep /tmp/requirements.txt /tmp/requirements.txt
RUN apk add --update --no-cache --virtual .build-deps alpine-sdk python3-dev musl-dev libffi-dev \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && apk --purge del .build-deps
COPY . /pilgrim/
WORKDIR /pilgrim
CMD ["main:app", "--host", "0.0.0.0", "--port", "80", "--proxy-headers", "--forwarded-allow-ips", "*"]
