redis:
	@docker run --rm --name test-redis -p 6379:6379 -d redis/redis-stack:latest

postgres:
	@docker run --rm --name test-postgres -p 5432:5432 -e POSTGRES_USER=local -e POSTGRES_PASSWORD=P@ssw0rd7 -e POSTGRES_DB=local -d postgres:14

req:
	@poetry export --without-hashes --format=requirements.txt > backend/requirements.txt