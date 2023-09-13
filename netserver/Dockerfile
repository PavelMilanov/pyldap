FROM golang:alpine as builder

WORKDIR /build

COPY . /build

RUN go build .


FROM alpine

WORKDIR /app

COPY --from=builder /build/netserver /app

ARG backend
ENV BACKEND_SERVER=$backend

ENTRYPOINT [ "./netserver" ]
