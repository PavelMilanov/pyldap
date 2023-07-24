package main

import (
	"fmt"
	"regexp"
	"strings"
)

// / Протокол для взаимодействия с клиентами. Cм. netclient.PyldapProtocol.
type PyldapProtocol struct {
	network []NetworkConfig
	system  SystemConfig
	time    string
}

// / Метод декодирует информацию от клиента. См. netclient.PyldapProtocol
func (protocol *PyldapProtocol) decode(bytes []byte) *PyldapProtocol {
	data := string(bytes)
	reHeader, _ := regexp.Compile(`Header:.*`)
	header := reHeader.FindString(data)
	protocol.system.hostName = header[8:]

	reBody, _ := regexp.Compile(`Body:.*`)
	body := reBody.FindString(data)
	trimdata := strings.TrimSpace(body[6:])
	bodyData := strings.Split(trimdata, " ")
	for _, item := range bodyData {
		intf := strings.Split(item, ",")
		protocol.network = append(protocol.network, NetworkConfig{
			ethName:  intf[0],
			mtu:      intf[1],
			netAddr:  intf[2],
			hardAddr: intf[3],
		})
	}
	reTime, _ := regexp.Compile(`Time:.*`)
	time := reTime.FindString(data)
	protocol.time = time[6:]

	fmt.Println(protocol)
	return protocol
}
