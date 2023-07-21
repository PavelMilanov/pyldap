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

func parseNetworkConfig() []byte {
	/// vlan3 1500 4c:52:62:3a:6a:2f 172.16.2.78/24

	var netData []byte
	interfaces, err := net.Interfaces()

	if err != nil {
		panic(err)
	}
	for _, intf := range interfaces {
		if intf.Name == "lo" { // пропускаем интерфейс loopback
			continue
		}
		hardAddress := intf.HardwareAddr.String()
		netAddresses, _ := intf.Addrs()
		mtu := strconv.Itoa(intf.MTU)
		var ip string
		/// убираем адрес ipv6
		for _, netAddress := range netAddresses {
			data := netAddress.String()
			matched, _ := regexp.MatchString(`[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}\/[0-9]{1,2}`, data)
			if matched {
				ip = data
			}
		}
		config := NetworkConfig{
			ethName:  intf.Name,
			mtu:      mtu,
			netAddr:  ip,
			hardAddr: hardAddress,
		}

		codedConfig := config.code()
		netData = append(netData, codedConfig...)
	}
	return netData
}

func parseHostName() []byte {
	cmd := exec.Command("hostname")
	out, _ := cmd.Output()
	return []byte(out)
}

func serverConnetion(connection net.Conn) string {
	defer connection.Close()
	var data []byte
	buffer := make([]byte, 400)
	netdata := parseNetworkConfig()
	hostdata := parseHostName()
	data = append(data, netdata...)
	data = append(data, hostdata...)
	connection.Write(data)
	serverData, err := connection.Read(buffer)
	connection.SetReadDeadline(time.Now().Add(time.Second * 5))
	if err != nil {
		fmt.Println("Error reading:", err.Error())
	}
	return string(buffer[:serverData])
}
