# make release web=192.168.1.1 v=1.2.3
web=
v=

release:
	@sed -i "s/listen_ip=*.*.*.*/listen_ip=$(web)/g" docker-compose.yaml
	@sed -i "s/version=v*.*.*/version=v$(v)/g" docker-compose.yaml
	@docker compose build --no-cache
	@docker compose up -d
