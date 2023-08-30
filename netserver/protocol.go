package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"regexp"
	"strings"
)

var BACKEND_SERVER = os.Getenv("BACKEND_SERVER")

// / Протокол для взаимодействия с клиентами. Cм. netclient.PyldapProtocol.
type ClientData struct {
	Network []string `json:"network"`
	System  string   `json:"system"`
	Time    string   `json:"time"`
}

// / Метод декодирует информацию от клиента. См. netclient.PyldapProtocol
func (protocol *ClientData) decode(bytes []byte) *ClientData {
	data := string(bytes)
	reEvent, _ := regexp.Compile(`Event:.*`)
	event := reEvent.FindString(data)
	switch event {
	case "config":
		reHeader, _ := regexp.Compile(`Header:.*`)
		header := reHeader.FindString(data)
		protocol.System = header[8:]
		reBody, _ := regexp.Compile(`Body:.*`)
		body := reBody.FindString(data)
		trimdata := strings.TrimSpace(body[6:])
		bodyData := strings.Split(trimdata, " ")
		for _, item := range bodyData {
			intf := strings.Split(item, ",")
			ipv4Data := fmt.Sprintf("%s %s %s %s", intf[0], intf[1], intf[2], intf[3])
			protocol.Network = append(protocol.Network, ipv4Data)
		}
		reTime, _ := regexp.Compile(`Time:.*`)
		time := reTime.FindString(data)
		protocol.Time = time[6:]
		return protocol
	case "message":
		reHeader, _ := regexp.Compile(`Header:.*`)
		header := reHeader.FindString(data)
		protocol.System = header[8:]
		reBody, _ := regexp.Compile(`Body:.*`)
		body := reBody.FindString(data)
		trimdata := strings.TrimSpace(body[6:])
		bodyData := strings.Split(trimdata, " ")
		fmt.Println(bodyData)
		reTime, _ := regexp.Compile(`Time:.*`)
		time := reTime.FindString(data)
		protocol.Time = time[6:]
		return protocol
	default:
		return protocol
	}
}

func (protocol *ClientData) send() int {

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
