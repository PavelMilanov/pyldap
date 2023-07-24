package main

// Тип для описния сетевого интерфейса клиентского устройства.
type NetworkConfig struct {
	ethName  string // - название интерфейса;
	mtu      string // - значение размера кадра интерфеса;
	netAddr  string // ip-адрес с маской;
	hardAddr string // mac-адрес.
}

// Тип для описания параметров ОС клиентского устройства.
type SystemConfig struct {
	hostName string // название устройства в сети
}
