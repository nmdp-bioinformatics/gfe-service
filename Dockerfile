FROM python:3.10-slim-buster

LABEL MAINTAINER="Pradeep Bashyal"

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY requirements-deploy.txt /app
RUN pip install --no-cache-dir -r requirements-deploy.txt

COPY api-spec.yaml /app/
COPY app.py /app/
COPY api.py /app/
COPY gfe_service /app/
COPY neo4j.yaml /app/

CMD ["gunicorn"  , "--bind", "0.0.0.0:8080", "--worker-tmp-dir", "/dev/shm", "app:app"]
