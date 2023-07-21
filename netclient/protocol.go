package main

import (
	"fmt"
	"time"
)

type PyldapProtocol struct {
	network []NetworkConfig
	system  SystemConfig
}

func (protocol *PyldapProtocol) code() []byte {
	var ipv4Data string
	for _, item := range protocol.network {
		if item.netAddr == "" {
			continue
		}
		ipv4Data += "{" + item.ethName + "," + item.mtu + "," + item.netAddr + "," + item.hardAddr + "} "
	}
	now := time.Now()
	message := fmt.Sprintf("Header: %s\rBody: %s\nTime: %d-%02d-%02d %02d:%02d\n", protocol.system.hostName, ipv4Data, now.Year(), now.Month(), now.Day(), now.Hour(), now.Minute())
	return []byte(message)
}
