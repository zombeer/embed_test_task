FROM python:3.10-alpine3.14

RUN apk add build-base \
    && apk add --no-cache python3 \ 
    && apk add --no-cache python3-dev

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app
ADD src .

ENV UVICORN_HOST=0.0.0.0
ENV UVICORN_PORT=8000

CMD uvicorn server:app