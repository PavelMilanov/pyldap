package main

import (
	"fmt"
	"log"
	"net"
)

func main() {

	const (
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

func clientConnection(connection net.Conn) {
	defer connection.Close() // закрываем сокет при выходе из функции

	buffer := make([]byte, 400) // буфер для чтения клиентских данных
	for {
		clientData, err := connection.Read(buffer)
		if err != nil {
			connection.Write(([]byte("0"))) // данные не приняты
			panic(err)
		}
		connection.Write(([]byte("1"))) // данные приняты успешно
		fmt.Println((string(buffer[:clientData])))
	}
}
