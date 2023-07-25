package main

import (
	"fmt"
	"io"
	"log"
	"net"
	"time"
)

func main() {

	var (
		SERVER = "192.168.1.2"
		PORT   = "8030"
	)

	listener, _ := net.Listen("tcp", SERVER+":"+PORT)
	info := fmt.Sprintf("Server listening on %s:%s", SERVER, PORT)
	log.Printf(info)
	for {
		conn, err := listener.Accept() // принимаем TCP-соединение от клиента и создаем новый сокет
		if err != nil {
			continue
		}
		go clientConnection(conn)
	}
}

// Основная логика взаимодействия с клиетами.
func clientConnection(connection net.Conn) {
	defer connection.Close() // закрываем сокет при выходе из функции

	buffer := make([]byte, 1024) // буфер для чтения клиентских данных
	for {
		clientData, err := connection.Read(buffer)
		connection.SetReadDeadline(time.Now().Add(time.Second * 5))
		if err != nil {
			connection.Write(([]byte("0"))) // данные не приняты
			if err == io.EOF {
				return
			}
			panic(err)
		}
		connection.Write(([]byte("1"))) // данные приняты успешно
		// fmt.Println((string(buffer[:clientData])))
		bytes := ClientData{}
		bytes.decode(buffer[:clientData])
		bytes.send()
	}
}
