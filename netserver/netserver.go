package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/gorilla/mux"
)

func ClientConfigHandler(w http.ResponseWriter, r *http.Request) {
	var config ClientConfig
	err := json.NewDecoder(r.Body).Decode(&config)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	config.send()
}

func ClientMessagesHandler(w http.ResponseWriter, r *http.Request) {
	var config ClientLog
	err := json.NewDecoder(r.Body).Decode(&config)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	config.send()
}

func ClientPingHandler(w http.ResponseWriter, r *http.Request) {
	host := r.URL.Query().Get("host")

	url := fmt.Sprintf("http://%s:8031/ping", host)
	client := http.Client{}

	request, err := http.NewRequest(http.MethodGet, url, nil)
	response, err := client.Do(request)
	if err != nil {
		panic(err)
	}
	defer response.Body.Close()
	log.Println(response.StatusCode)
}

func main() {

	const PORT = ":8030"
	router := mux.NewRouter()
	server := &http.Server{
		Addr:         PORT,
		WriteTimeout: time.Second * 15,
		ReadTimeout:  time.Second * 15,
		IdleTimeout:  time.Second * 60,
		Handler:      router,
	}
	router.HandleFunc("/config", ClientConfigHandler).Methods("POST")
	router.HandleFunc("/messages", ClientMessagesHandler).Methods("POST")
	router.HandleFunc("/ping", ClientPingHandler).Methods("GET")

	fmt.Printf("Starting server on port %v\n", PORT)
	err := server.ListenAndServe()
	if err != nil {
		log.Println(err)
	}
}
