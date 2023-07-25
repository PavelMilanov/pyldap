FROM golang:alpine as builder

ARG server
ARG backend

WORKDIR /build

COPY . /build

ENV SERVER=${server}
ENV BACKEND_SERVER=${backend}

RUN go build .


FROM alpine

WORKDIR /app

COPY --from=builder /build/netserver /app

ENTRYPOINT [ "./netserver" ]
