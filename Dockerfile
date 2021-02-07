FROM python:3.9-alpine

COPY ./requirements.txt /tmp
RUN pip install --no-cache-dir -r /tmp/requirements.txt gunicorn==20.0.4

COPY . /opt/project
WORKDIR /opt/project
CMD /usr/local/bin/gunicorn --access-logfile - --error-logfile - --workers $NPROC --threads $NTHREAD -b :$PORT app:app