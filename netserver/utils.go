package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"
)

var BACKEND_SERVER = os.Getenv("BACKEND_SERVER")

// Структура для преобразования и передачи валидных данных на сервер бекенда.
type ClientConfig struct {
	Network []string `json:"network"`
	System  string   `json:"system"`
	Time    string   `json:"time"`
}

// Метод форматирует данные в JSON-формат для передачи на сервер бекенда.
// Пример:
//
//	{
//	       "network": [
//	               "en0,1500,192.168.1.2/24,3c:a6:f6:b3:bf:e1",
//	               "en1,1500,192.168.1.6/24,3c:a6:f6:af:ba:e1",
//	               "bridge100,1500,192.168.193.1/24,3e:a6:f6:3b:1a:64",
//	               "bridge101,1500,172.16.184.1/24,3e:a6:f6:3b:1a:65"
//	       ],
//	       "system": "iMac-pavel-milanov.local",
//			"time": "2023-08-02 19:31"
//	}
func (config *ClientConfig) send() {

	url := fmt.Sprintf("http://%s:8000/api/v1/network/netclient", "localhost")
	now := time.Now()
	datalog := fmt.Sprintf("%d-%02d-%02d %02d:%02d", now.Year(), now.Month(), now.Day(), now.Hour(), now.Minute())
	config.Time = datalog
	data, err := json.MarshalIndent(config, "", "\t")
	if err != nil {
		panic(err)
	}
	client := http.Client{}
	log.Println(string(data))
	request, err := http.NewRequest(http.MethodPost, url, bytes.NewBuffer(data))
	request.Header.Set("Content-Type", "application/json; charset=UTF-8")

	response, err := client.Do(request)
	if err != nil {
		panic(err)
	}
	defer response.Body.Close()
	log.Println(response.StatusCode)
}
