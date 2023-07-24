package main

// Тип для описния сетевого интерфейса клиентского устройства. См. netclient.NetworkConfig.
type NetworkConfig struct {
	ethName  string // - название интерфейса;
	mtu      string // - значение размера кадра интерфеса;
	netAddr  string // ip-адрес с маской;
	hardAddr string // mac-адрес.
}

// Тип для описания параметров ОС клиентского устройства. См. netclient.SystemConfig.
type SystemConfig struct {
	hostName string // название устройства в сети
}
