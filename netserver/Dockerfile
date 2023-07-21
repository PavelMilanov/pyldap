FROM golang:alpine as builder

WORKDIR /build

COPY . /build

RUN go build -o netserver netserver.go


FROM alpine

WORKDIR /app

COPY --from=builder /build/netserver /app

ENTRYPOINT [ "./netserver" ]
