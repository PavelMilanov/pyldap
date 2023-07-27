FROM golang:alpine as builder

ARG listen_netserver
ARG backend

WORKDIR /build

COPY . /build

RUN echo "SERVER=${listen_netserver}}" > .env && echo "BACKEND_SERVER=${backend}}" >> .env && go build .


FROM alpine

WORKDIR /app

COPY --from=builder /build/netserver /app

ENTRYPOINT [ "./netserver" ]
