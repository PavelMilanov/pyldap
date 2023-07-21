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
		SERVER = "192.168.1.2"
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

func parseNetworkConfig() []NetworkConfig {
	/// vlan3 1500 4c:52:62:3a:6a:2f 172.16.2.78/24

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
			// fmt.Println(config)
			// codedConfig := config.code()
			netData = append(netData, config)
		}
	}
	return netData
}
func parseHostName() SystemConfig {
	cmd := exec.Command("hostname")
	out, _ := cmd.Output()
	return SystemConfig{hostName: string(out)}
}

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
