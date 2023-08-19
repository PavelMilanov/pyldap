package main

import (
	"bytes"
	"context"
	"flag"
	"fmt"
	"log"
	"net"
	"net/http"
	"os"
	"os/exec"
	"os/signal"
	"regexp"
	"strconv"
	"strings"
	"time"

	"github.com/gorilla/mux"
)

var (
	NET_SERVER      = os.Getenv("NET_SERVER")
	NET_SERVER_PORT = os.Getenv("NET_SERVER_PORT")
)

func PingHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
}

func main() {

	const (
		PORT = ":8031"
	)
	var wait time.Duration
	flag.DurationVar(&wait, "graceful-timeout", time.Second*15, "the duration for which the server gracefully wait for existing connections to finish - e.g. 15s or 1m")
	flag.Parse()

	router := mux.NewRouter()
	server := &http.Server{
		Addr:    PORT,
		Handler: router,
	}

	router.HandleFunc("/ping", PingHandler).Methods("GET")

	status := sendConfig()
	go sendMessage("login")
	if status != "ok" {
		log.Println(status)
	}
	fmt.Printf("Starting server on port %v\n", PORT)
	go func() {
		err := server.ListenAndServe()
		if err != nil {
			log.Println(err)
		}
	}()
	c := make(chan os.Signal, 1)
	// We'll accept graceful shutdowns when quit via SIGINT (Ctrl+C)
	// SIGKILL, SIGQUIT or SIGTERM (Ctrl+/) will not be caught.
	signal.Notify(c, os.Interrupt)

	// Block until we receive our signal.
	<-c
	sendMessage("shutdown")
	ctx, cancel := context.WithTimeout(context.Background(), wait)
	defer cancel()
	server.Shutdown(ctx)
	os.Exit(0)
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

	url := fmt.Sprintf("http://%s:%s/config", NET_SERVER, NET_SERVER_PORT)
	client := http.Client{}
	request, err := http.NewRequest(http.MethodPost, url, bytes.NewBuffer(message))
	request.Header.Set("Content-Type", "application/json; charset=UTF-8")

	response, err := client.Do(request)
	if err != nil {
		return err.Error()
	}
	defer response.Body.Close()
	return "ok"
}

// Отправка информации на сервер.
func sendMessage(text string) {
	hostdata := parseHostName()
	data := ClientLog{SystemName: hostdata.hostName, Message: text}
	message := data.code()

	url := fmt.Sprintf("http://%s:%s/messages", NET_SERVER, NET_SERVER_PORT)
	client := http.Client{}
	request, err := http.NewRequest(http.MethodPost, url, bytes.NewBuffer(message))
	request.Header.Set("Content-Type", "application/json; charset=UTF-8")

	response, err := client.Do(request)
	if err != nil {
		log.Println(err)
	}
	defer response.Body.Close()
}
