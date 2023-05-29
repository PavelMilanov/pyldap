redis:
	@docker run --rm --name redis -p 6379:6379 -d redis:7

postgres:
	@docker run --rm --name postgres -p 5432:5432 -e POSTGRES_USER=local -e POSTGRES_PASSWORD=P@ssw0rd7 -e POSTGRES_DB=local -d postgres:14
req:
	@poetry export --without-hashes --format=requirements.txt > pyldap/requirements.txt