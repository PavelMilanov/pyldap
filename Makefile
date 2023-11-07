# make release domain=local.test v=1.2.3
# ip=
domain=
v=

release:
	@sed -i "s/listen_domain=[a-z]/${domain}/g" docker-compose.yaml
	@sed -i "s/version=v*.*.*/version=v${v}/g" docker-compose.yaml
	@docker compose build --no-cache
	@docker compose up -d
