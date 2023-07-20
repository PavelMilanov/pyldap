FROM python:3.11-alpine as builder

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev curl

COPY requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


FROM python:3.11-alpine

WORKDIR /server

COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*
COPY . /server

ENTRYPOINT ["sh", "init.sh"]
