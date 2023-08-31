package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"regexp"
	"strings"
)

var BACKEND_SERVER = os.Getenv("BACKEND_SERVER")

type ClientData struct {
	// Протокол для взаимодействия с клиентами. Cм. netclient.PyldapProtocol.
	Network []string `json:"network,omitempty"`
	Message string   `json:"message,omitempty"`
	System  string   `json:"system"`
	Time    string   `json:"time"`
}

func (protocol *ClientData) decode(bytes []byte) {
	// Метод декодирует информацию от клиента. См. netclient.PyldapProtocol
	// Пример одного фрайма:
	//
	//Event: config
	//Header: iMac-pavel-milanov.local
	//Body: en0,1500,192.168.1.2/24,3c:a6:f6:b3:bf:e1 en1,1500,192.168.1.6/24,3c:a6:f6:af:ba:e1 bridge100,1500,192.168.193.1/24,3e:a6:f6:3b:1a:64 bridge101,1500,172.16.184.1/24,3e:a6:f6:3b:1a:65
	//Time: 2023-08-30 23:45
	//...
	//Event: message
	//Header: iMac-pavel-milanov.local
	//Body: login
	//Time: 2023-08-30 23:45
	//...
	data := string(bytes)
	frames := strings.Split(data, "...") // Разбивает общий фрэйм на отдельные сообщения по метке.
	for _, frame := range frames[:len(frames)-1] {
		reEvent, _ := regexp.Compile(`Event:.*`)
		event := reEvent.FindString(frame)[7:]
		reHeader, _ := regexp.Compile(`Header:.*`)
		header := reHeader.FindString(frame)
		if strings.HasSuffix(header[8:], "\r") { // Убираем символ \r в конце строки, если он присутсвует
			protocol.System = header[8 : len(header)-1]
		}
		reTime, _ := regexp.Compile(`Time:.*`)
		time := reTime.FindString(frame)
		protocol.Time = time[6:]

		switch event {
		case "config":
			reBody, _ := regexp.Compile(`Body:.*`)
			body := reBody.FindString(frame)
			trimdata := strings.TrimSpace(body[6:])
			bodyData := strings.Split(trimdata, " ")
			for _, item := range bodyData {
				intf := strings.Split(item, ",")
				ipv4Data := fmt.Sprintf("%s %s %s %s", intf[0], intf[1], intf[2], intf[3])
				protocol.Network = append(protocol.Network, ipv4Data)
			}
			status := protocol.sendConfig()
			log.Println(status)
		case "message":
			reBody, _ := regexp.Compile(`Body:.*`)
			body := reBody.FindString(frame)[6:]
			protocol.Message = body
			status := protocol.sendMessage()
			log.Println(status)
		}
	}
}

func (protocol *ClientData) sendConfig() int {
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
	//			"time": "2023-07-26 17:06"
	//	}
	config := &ClientData{
		Network: protocol.Network,
		System:  protocol.System,
		Time:    protocol.Time,
	}
	url := fmt.Sprintf("http://%s:8000/api/v1/network/netclient", BACKEND_SERVER)
	data, err := json.MarshalIndent(config, "", "\t")
	if err != nil {
		panic(err)
	}
	client := http.Client{}
	request, err := http.NewRequest(http.MethodPost, url, bytes.NewBuffer(data))
	request.Header.Set("Content-Type", "application/json; charset=UTF-8")

	response, err := client.Do(request)
	if err != nil {
		panic(err)
	}
	defer response.Body.Close()
	return response.StatusCode
}

func (protocol *ClientData) sendMessage() int {
	// Метод форматирует данные в JSON-формат для передачи на сервер бекенда.
	// Пример:
	//
	// {
	//    "system": "iMac-pavel-milanov.local",
	//    "message": "login",
	//    "time": "2023-08-26 00:14"
	// }
	config := &ClientData{
		Message: protocol.Message,
		System:  protocol.System,
		Time:    protocol.Time,
	}
	url := fmt.Sprintf("http://%s:8000/api/v1/network/netclient/messages", BACKEND_SERVER)
	data, err := json.MarshalIndent(config, "", "\t")
	if err != nil {
		panic(err)
	}
	client := http.Client{}
	request, err := http.NewRequest(http.MethodPost, url, bytes.NewBuffer(data))
	request.Header.Set("Content-Type", "application/json; charset=UTF-8")

	response, err := client.Do(request)
	if err != nil {
		panic(err)
	}
	defer response.Body.Close()
	return response.StatusCode
}
