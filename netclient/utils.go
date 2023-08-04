package main

import (
	"encoding/json"
	"log"
)

// Структура для преобразования и передачи валидных данных на сервер.
// Включает в себя параметры всех сетевых интерфейсов клиента: eth, ip, mtu, mac. (Тип NetworkConfig)
// Параметры операционной системы: hostname. (Тип SystemConfig)
type ClientConfig struct {
	network         []NetworkConfig
	system          SystemConfig
	NetworkSettings []string `json:"network"`
	SystemName      string   `json:"system"`
}

// Метод форматирует данные в JSON-формат для передачи на сервер.
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
//	}
func (config *ClientConfig) code() []byte {
	var ipv4Data []string
	for _, item := range config.network {
		if item.netAddr == "" { // усли интерфейс не имеет ip - не передаем
			continue
		}
		ipv4Data = append(ipv4Data, item.ethName+","+item.mtu+","+item.netAddr+","+item.hardAddr)
	}
	config.NetworkSettings = ipv4Data
	config.SystemName = config.system.hostName
	codeData, _ := json.MarshalIndent(config, "", "\t")
	log.Println(string(codeData))
	return codeData
}
