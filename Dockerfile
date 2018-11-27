FROM python:3.6

ADD Pipfile app/Pipfile 
ADD Pipfile.lock app/Pipfile.lock

WORKDIR /app

RUN python3 -m venv .venv \
 && source .venv/bin/activate \
 && pip install --upgrade pip==18.0 pipenv \
 && pipenv sync


