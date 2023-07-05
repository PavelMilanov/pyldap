
ip=
v=

release:
	@sed -i "s/listen_ip=*.*.*.*/listen_ip=$(ip)/g" docker-compose.yaml
	@sed -i "s/version=v*.*.*/version=v$(v)/g" docker-compose.yaml
	@docker compose up build
	@docker compose up -d
