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
		SERVER = "localhost"
		PORT   = "8030"
	)

	listener, _ := net.Listen("tcp", SERVER+":"+PORT)
	defer listener.Close()
	info := fmt.Sprintf("Server listening on %s:%s", SERVER, PORT)
	log.Printf(info)
	for {
		conn, err := listener.Accept() // принимаем TCP-соединение от клиента и создаем новый сокет
		if err != nil {
			continue
		}
		go clientConnection(conn)
	}
	// }
}

func clientConnection(connection net.Conn) {
	// Основная логика взаимодействия с клиетами.
	defer connection.Close() // закрываем сокет при выходе из функции

	buffer := make([]byte, 1024) // буфер для чтения клиентских данных
	for {
		connection.SetReadDeadline(time.Now().Add(time.Second * 5))
		client, err := connection.Read(buffer)
		if err != nil {
			connection.Write(([]byte("0"))) // данные не приняты
			if err == io.EOF {
				return
			}
			panic(err)
		}
<<<<<<< HEAD
=======
		// connection.Write(([]byte("1"))) // данные приняты успешно
		// fmt.Println((string(buffer[:client])))
>>>>>>> 479c6f2 (rebuild backend-netserver-netclient API)
		bytes := ClientData{}
		bytes.decode(buffer[:client])
	}
}
