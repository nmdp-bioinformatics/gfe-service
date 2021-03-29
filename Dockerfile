FROM nmdpbioinformatics/py-gfe:1.1.3

LABEL MAINTAINER NMDP Bioinformatics https://github.com/nmdp-bioinformatics

WORKDIR /app

COPY requirements-deploy.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY api /app/api
COPY spec /app/spec

COPY main.py /app/
COPY neo4j.yaml /app/

CMD [ "python", "main.py" ]
