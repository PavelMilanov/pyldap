package main

import (
	"log"
	"net"
	"os"
	"os/exec"
	"regexp"
	"strconv"
	"strings"
	"time"

	"github.com/kardianos/service"
)

var (
	SERVER = "172.16.2.78"
	PORT   = "8030"
)
var logger service.Logger

type program struct{}

func (p *program) Start(s service.Service) error {
	// Start should not block. Do the actual work async.
	go p.run()
	return nil
}
func (p *program) run() {
	// Do work here
	conn, err := net.Dial("tcp", SERVER+":"+PORT)
	if err != nil {
		panic(err)
	}
	netdata := parseNetworkConfig()
	hostdata := parseHostName()
	data := PyldapProtocol{network: netdata, system: hostdata}
	message1 := data.code("config", "")
	message2 := data.code("message", "login")
	serverConnetion(conn, message1, message2)
	// message := data.code("message", "login")
	// serverConnetion(conn, message)
}

func (p *program) Stop(s service.Service) error {
	// Stop should not block. Return with a few seconds.
	// sendMessage("shutdown")
	<-time.After(time.Second * 3)
	return nil
}
func main() {
	svcConfig := &service.Config{
		Name:        "NetClient",
		DisplayName: "NetClient V1",
		Description: "NetClient service for customers",
	}

	prg := &program{}
	s, err := service.New(prg, svcConfig)
	if err != nil {
		log.Fatal(err)
	}
	if len(os.Args) > 1 {
		err = service.Control(s, os.Args[1])
		if err != nil {
			log.Fatal(err)
		}
		return
	}
	logger, err = s.Logger(nil)
	if err != nil {
		log.Fatal(err)
	}
	err = s.Run()
	if err != nil {
		logger.Error(err)
	}
}

func parseNetworkConfig() []NetworkConfig {
	// Функция собирает и форматирует параметры сетевых интерфейсов.
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

func parseHostName() SystemConfig {
	// Функция собирает и форматирует параметры ОС.
	cmd := exec.Command("hostname")
	out, _ := cmd.Output()
	data := strings.Trim(string(out), "\n")
	return SystemConfig{hostName: data}
}

func serverConnetion(connection net.Conn, messages ...[]byte) {
	// Основная логика взаимодействия с сервером.
	defer connection.Close()

	// buffer := make([]byte, 1024)
	connection.SetReadDeadline(time.Now().Add(time.Second * 5))
	for _, message := range messages {
		connection.Write([]byte(message))
		// _, err := connection.Read(buffer)
		// if err != nil {
		// 	fmt.Println("Error reading:", err.Error())
		// }
	}
	// connection.Write([]byte("1"))
}
