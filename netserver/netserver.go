package main

import (
	"encoding/json"
	"fmt"
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
	r := mux.NewRouter()
	r.HandleFunc("/logon", ClientLogonHandler)

	fmt.Printf("Starting server on port %v\n", PORT)
	http.ListenAndServe(PORT, r)
}
