redis:
	@docker run --rm --name test-redis -p 6379:6379 -d redis:7

postgres:
	@docker run --rm --name test-postgres -p 5432:5432 -e POSTGRES_USER=local -e POSTGRES_PASSWORD=P@ssw0rd7 -e POSTGRES_DB=local -d postgres:14

mongo:
	@docker run --rm --name test-mongo -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=local -e MONGO_INITDB_ROOT_PASSWORD=local -d mongo

req:
	@poetry export --without-hashes --format=requirements.txt > backend/requirements.txt