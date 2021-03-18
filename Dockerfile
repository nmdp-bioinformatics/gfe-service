FROM nmdpbioinformatics/py-gfe

LABEL maintainer="nmdp-bioinformatics"

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]

CMD [ "main.py" ]
