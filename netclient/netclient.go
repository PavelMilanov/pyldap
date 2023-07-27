package main

import (
	"fmt"
	"log"
	"net"
	"os"
	"os/exec"
	"regexp"
	"strconv"
	"strings"
	"time"
)

func main() {

	var (
		SERVER = "10.0.102.130"
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
		isLoopback, _ := regexp.MatchString(`(?i)^lo`, intf.Name) // пропускаем интерфейс loopback || пропускаем многие дефолтные интерфейсы не из одного слова [Loopback Pseudo-Interface 1],[Сетевое подключение Bluetooth]
		if isLoopback || len(strings.Fields(intf.Name)) > 1 {
			continue
		}
		hardAddress := intf.HardwareAddr.String()
		netAddresses, _ := intf.Addrs()
		mtu := strconv.Itoa(intf.MTU)
		var ip string
		/// убираем адрес ipv6
		for _, netAddress := range netAddresses {
			data := netAddress.String()
			isIpv4, _ := regexp.MatchString(`[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\/[0-9]{1,2}`, data)
			if isIpv4 {
				ip = data
			} else {
				continue
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
