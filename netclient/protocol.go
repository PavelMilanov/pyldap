package main

import (
	"fmt"
	"time"
)

type PyldapProtocol struct {
	// Протокол для передачи служебной информации в архитектуре Pyldap.
	// Включает в себя параметры всех сетевых интерфейсов клиента: eth, ip, mtu, mac. (Тип NetworkConfig)
	// Параметры операционной системы: hostname. (Тип SystemConfig)
	network []NetworkConfig
	system  SystemConfig
}

func (protocol *PyldapProtocol) code(kind string, event string) []byte {
	switch kind {
	case "config":
		data := protocol.sendConfig(kind)
		return data
	case "message":
		data := protocol.sendMessage(kind, event)
		return data
	default:
		return []byte("error")
	}
}

func (protocol *PyldapProtocol) sendConfig(event string) []byte {
	// Метод кодирует всю полученную информацию в формат, предписывающий протоколом.
	// Пример:
	//
	//	Header: iMac-pavel-milanov.local
	//	Body: {en0,1500,192.168.1.2/24,3c:a6:f6:b3:bf:e1} {en0,1500,192.168.1.2/24,3c:a6:f6:b3:bf:e1}
	//	Time: 2023-07-22 00:02
	var ipv4Data string
	for _, item := range protocol.network {
		if item.netAddr == "" { // если интерфейс не имеет ip - не передаем
			continue
		}
		ipv4Data += item.ethName + "," + item.mtu + "," + item.netAddr + "," + item.hardAddr + " "
	}
	now := time.Now()
	data := fmt.Sprintf("Event: %s\nHeader: %s\nBody: %s\nTime: %d-%02d-%02d %02d:%02d\nEnd\n", event, protocol.system.hostName, ipv4Data, now.Year(), now.Month(), now.Day(), now.Hour(), now.Minute())
	fmt.Println(data)
	return []byte(data)
}

func (protocol *PyldapProtocol) sendMessage(event string, text string) []byte {
	// Функция отправки системных сообщений на сервер.
	now := time.Now()
	data := fmt.Sprintf("Event: %s\nHeader: %s\nBody: %s\nTime: %d-%02d-%02d %02d:%02d\nEnd", event, protocol.system.hostName, text, now.Year(), now.Month(), now.Day(), now.Hour(), now.Minute())
	fmt.Println(data)
	return []byte(data)
}
