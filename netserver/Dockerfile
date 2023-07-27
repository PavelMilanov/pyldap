FROM golang:alpine as builder

WORKDIR /build

COPY . /build

RUN go build .


FROM alpine

WORKDIR /app

COPY --from=builder /build/netserver /app

ARG listen_netserver
ARG backend

ENV SERVER=$listen_netserver
ENV BACKEND_SERVER=$backend
ENTRYPOINT [ "./netserver" ]
