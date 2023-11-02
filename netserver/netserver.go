package main

import (
	"fmt"
	"io"
	"log"
	"net"
	"os"
	"time"
)

var (
	SERVER = "0.0.0.0"
	PORT   = "8030"
)

func main() {
	command := os.Args[1]
	switch command {
	case "ping":
		connection, err := net.Dial("tcp", "localhost"+":"+"8030")
		if err != nil {
			panic(err)
		}
		buffer := make([]byte, 1024)

		message := healthCheck()
		defer connection.Close()
		connection.Write(message)
		data, err := connection.Read(buffer)
		if data != 1 {
			os.Exit(1) // если не пришел ответ, завершаем процесс с ошибкой
		}
		log.Print("pong")
	default:
		listener, _ := net.Listen("tcp", SERVER+":"+PORT)
		defer listener.Close()
		info := fmt.Sprintf("Server listening on %s:%s", SERVER, PORT)
		log.Print(info)
		for {
			conn, err := listener.Accept() // принимаем TCP-соединение от клиента и создаем новый сокет
			if err != nil {
				continue
			}
			go clientConnection(conn)
		}
	}
}

func healthCheck() []byte {
	now := time.Now()
	data := fmt.Sprintf(
		"Event: check\nHeader: check\nBody: check\nTime: %d-%02d-%02d %02d:%02d\n...",
		now.Year(),
		now.Month(),
		now.Day(),
		now.Hour(),
		now.Minute())
	return []byte(data)
}

func clientConnection(connection net.Conn) {
	// Основная логика взаимодействия с клиетами.
	defer connection.Close() // закрываем сокет при выходе из функции

	buffer := make([]byte, 1024) // буфер для чтения клиентских данных
	for {
		connection.SetReadDeadline(time.Now().Add(time.Second * 5))
		client, err := connection.Read(buffer)
		if err != nil {
			connection.Write([]byte("0")) // данные не приняты
			if err == io.EOF {
				return
			}
			panic(err)
		}
		bytes := ClientData{}
		bytes.decode(buffer[:client], connection)
	}
}
