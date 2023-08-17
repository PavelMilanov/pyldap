package main

import (
	"bytes"
	"fmt"
	"log"
	"net"
	"net/http"
	"os/exec"
	"regexp"
	"strconv"
	"strings"
)

func main() {

	const (
		PORT = ":8031"
	)

	server := &http.Server{Addr: PORT, Handler: nil}
	fmt.Printf("Starting server on port %v\n", PORT)
	status := sendConfig()
	if status != "ok" {
		log.Println(status)
	}
	err := server.ListenAndServe()
	if err != nil {
		log.Println(err)
	}

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
	data := strings.Trim(string(out), "\n")
	return SystemConfig{hostName: data}
}

// Отправка конфигурации на сервер при включение хоста.
func sendConfig() string {
	netdata := parseNetworkConfig()
	hostdata := parseHostName()
	data := ClientConfig{network: netdata, system: hostdata}
	message := data.code()
	url := "http://localhost:8030/logon"
	client := http.Client{}
	request, err := http.NewRequest(http.MethodPost, url, bytes.NewBuffer(message))
	request.Header.Set("Content-Type", "application/json; charset=UTF-8")

	response, err := client.Do(request)
	if err != nil {
		// log.Println(err)
		return err.Error()
	}
	defer response.Body.Close()
	// log.Println(response.StatusCode)
	return "ok"
}
