package main

type NetworkConfig struct {
	ethName  string
	mtu      string
	netAddr  string
	hardAddr string
}

func (config *NetworkConfig) code() []byte {
	// data := []byte(config.ethName + config.mtu + config.netAddr + config.hardAddr)

	return []byte(config.ethName + config.mtu + config.netAddr + config.hardAddr)
}
