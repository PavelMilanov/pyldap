package main

import (
	"fmt"
	"io"
	"log"
	"net"
	"time"
)

// func ClientConfigHandler(w http.ResponseWriter, r *http.Request) {
// 	var config ClientConfig
// 	err := json.NewDecoder(r.Body).Decode(&config)
// 	if err != nil {
// 		http.Error(w, err.Error(), http.StatusBadRequest)
// 		return
// 	}
// 	config.send()
// }

// func ClientMessagesHandler(w http.ResponseWriter, r *http.Request) {
// 	var config ClientLog
// 	err := json.NewDecoder(r.Body).Decode(&config)
// 	if err != nil {
// 		http.Error(w, err.Error(), http.StatusBadRequest)
// 		return
// 	}
// 	config.send()
// }

// func ClientPingHandler(w http.ResponseWriter, r *http.Request) {
// 	host := r.URL.Query().Get("host")
// 	url := fmt.Sprintf("http://%s:8031/ping", host)
// 	client := http.Client{}

// 	request, err := http.NewRequest(http.MethodGet, url, nil)
// 	response, err := client.Do(request)
// 	if err != nil {
// 		log.Println(err)
// 		return
// 	}
// 	defer response.Body.Close()
// }

// func HealthCheckHandler(w http.ResponseWriter, r *http.Request) {
// 	w.WriteHeader(http.StatusOK)
// }

func main() {

	// const PORT = ":8030"
	// router := mux.NewRouter()
	// server := &http.Server{
	// 	Addr:         PORT,
	// 	WriteTimeout: time.Second * 15,
	// 	ReadTimeout:  time.Second * 15,
	// 	IdleTimeout:  time.Second * 60,
	// 	Handler:      router,
	// }
	// router.HandleFunc("/config", ClientConfigHandler).Methods("POST")
	// router.HandleFunc("/messages", ClientMessagesHandler).Methods("POST")
	// router.HandleFunc("/ping", ClientPingHandler).Methods("GET")
	// router.HandleFunc("/check", HealthCheckHandler).Methods("GET")

	// fmt.Printf("Starting server on port %v\n", PORT)
	// err := server.ListenAndServe()
	// if err != nil {
	// 	log.Println(err)
	var (
		SERVER = "0.0.0.0"
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
		// connection.Write(([]byte("1"))) // данные приняты успешно
		fmt.Println((string(buffer[:client])))
		bytes := ClientData{}
		// fmt.Println(bytes)
		bytes.decode(buffer[:client])
		// resp := bytes.send()
		// fmt.Println(resp)
	}
}
