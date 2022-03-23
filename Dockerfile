# syntax=docker/dockerfile:1

FROM python:3.7-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN python3 -m spacy download en_core_web_sm

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]