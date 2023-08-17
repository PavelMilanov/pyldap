package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

func ClientLogonHandler(w http.ResponseWriter, r *http.Request) {
	var config ClientConfig
	err := json.NewDecoder(r.Body).Decode(&config)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	config.send()
}

func main() {

	const PORT = ":8030"
	router := mux.NewRouter()
	server := &http.Server{
		Addr:    PORT,
		Handler: router,
	}

	router.HandleFunc("/logon", ClientLogonHandler)

	fmt.Printf("Starting server on port %v\n", PORT)
	err := server.ListenAndServe()
	if err != nil {
		log.Println(err)
	}
}
