package main

import (
	"fmt"
	"log"
	"os"
	"time"
)

// Протокол для передачи служебной информации в архитектуре Pyldap.
// Включает в себя параметры всех сетевых интерфейсов клиента: eth, ip, mtu, mac. (Тип NetworkConfig)
// Параметры операционной системы: hostname. (Тип SystemConfig)
type PyldapProtocol struct {
	network []NetworkConfig
	system  SystemConfig
}

// Метод кодирует всю полученную информацию в формат, предписывающий протоколом.
// Пример:
//
//	Header: iMac-pavel-milanov.local
//	Body: {en0,1500,192.168.1.2/24,3c:a6:f6:b3:bf:e1} {en0,1500,192.168.1.2/24,3c:a6:f6:b3:bf:e1}
//	Time: 2023-07-22 00:02
func (protocol *PyldapProtocol) code() []byte {
	var ipv4Data string
	for _, item := range protocol.network {
		if item.netAddr == "" { // усли интерфейс не имеет ip - не передаем
			continue
		}
		ipv4Data += item.ethName + "," + item.mtu + "," + item.netAddr + "," + item.hardAddr + " "
	}
	now := time.Now()
	message := fmt.Sprintf("Header: %s\rBody: %s\nTime: %d-%02d-%02d %02d:%02d\n", protocol.system.hostName, ipv4Data, now.Year(), now.Month(), now.Day(), now.Hour(), now.Minute())
	file, err := os.OpenFile("info.log", os.O_RDWR|os.O_CREATE, 0666)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	logfile := log.New(file, message, log.Ldate|log.Ltime)
	logfile.Println()
	return []byte(message)
}
