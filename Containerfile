FROM docker.io/python:3.11-alpine

COPY requirements.txt /requirements.txt

RUN set -eu \
	&& pip install --no-cache-dir --upgrade -r /requirements.txt \
	&& find /usr/lib/ -name '__pycache__' -print0 | xargs -0 -n1 rm -rf \
	&& find /usr/lib/ -name '*.pyc' -print0 | xargs -0 -n1 rm -rf

COPY main.py /main.py

ENTRYPOINT ["python", "/main.py"]
