FROM python:3.12-slim-bullseye as base

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt update && \
   apt install --no-install-recommends --no-install-suggests --assume-yes \
    gcc \
    python3-dev \
    libpq-dev \
    libmagic1 \
    curl

RUN python -m pip install --upgrade pip

ENV app app
RUN mkdir /$app
COPY requirements.txt /$app

WORKDIR /$app

RUN pip install -r requirements.txt

ADD src src

FROM base as service

EXPOSE 8080

CMD python3 -m src

FROM base as migrator

ADD migrations migrations
ADD alembic.ini .

CMD alembic upgrade head

FROM base as tester

add tests tests

CMD pytest tests
