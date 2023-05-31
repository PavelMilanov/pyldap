FROM python:3.11-alpine

RUN apk add --no-cache gcc musl-dev python3-dev libffi-dev
COPY . /server/
WORKDIR /server

RUN pip install -r requirements.txt
ENTRYPOINT sh init.sh
