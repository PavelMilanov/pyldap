FROM golang:alpine as builder

ARG listen_netserver
ARG backend

WORKDIR /build

COPY . /build

RUN go build .


FROM alpine

WORKDIR /app

COPY --from=builder /build/netserver /app

ENV SERVER=${listen_netserver}
ENV BACKEND_SERVER=${backend}
ENTRYPOINT [ "./netserver" ]
