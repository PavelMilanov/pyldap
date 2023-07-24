package main

import (
	"fmt"
	"log"
	"net"
	"os"
	"os/exec"
	"regexp"
	"strconv"
	"time"
)

func main() {

	const (
		SERVER = "172.16.2.78"
		PORT   = "8030"
	)

	conn, err := net.Dial("tcp", SERVER+":"+PORT)
	if err != nil {
		panic(err)
	}
	status := serverConnetion(conn)
	if status == "1" {
		log.Println(status)
		os.Exit(0)
	}
	os.Exit(1)
}

// Собирает и форматирует параметры сетевых интерфейсов.
func parseNetworkConfig() []NetworkConfig {
	var netData []NetworkConfig
	interfaces, err := net.Interfaces()

	if err != nil {
		panic(err)
	}
	for _, intf := range interfaces {
		matched, _ := regexp.MatchString(`^lo`, intf.Name)
		if matched { // пропускаем интерфейс loopback
			continue
		}
		hardAddress := intf.HardwareAddr.String()
		netAddresses, _ := intf.Addrs()
		mtu := strconv.Itoa(intf.MTU)
		var ip string
		/// убираем адрес ipv6
		for _, netAddress := range netAddresses {
			data := netAddress.String()
			matched, _ := regexp.MatchString(`[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\/[0-9]{1,2}`, data)
			if matched {
				ip = data
			}
			config := NetworkConfig{
				ethName:  intf.Name,
				mtu:      mtu,
				netAddr:  ip,
				hardAddr: hardAddress,
			}
			netData = append(netData, config)
		}
	}
	return netData
}

// Собирает и форматирует параметры ОС.
func parseHostName() SystemConfig {
	cmd := exec.Command("hostname")
	out, _ := cmd.Output()
	return SystemConfig{hostName: string(out)}
}

// Основная логика взаимодействия с сервером.
func serverConnetion(connection net.Conn) string {
	defer connection.Close()
	buffer := make([]byte, 1024)
	netdata := parseNetworkConfig()
	hostdata := parseHostName()
	data := PyldapProtocol{network: netdata, system: hostdata}
	message := data.code()
	connection.Write([]byte(message))
	serverData, err := connection.Read(buffer)
	connection.SetReadDeadline(time.Now().Add(time.Second * 5))
	if err != nil {
		fmt.Println("Error reading:", err.Error())
	}
	return string(buffer[:serverData])
}
