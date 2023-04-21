redis:
	@docker run --rm --name redis -p 6379:6379 -d redis:7

postgres:
	@docker run --rm --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=P@ssw0rd7 -d postgres:14