from tortoise import Tortoise

TORTOISE_ORM = {
        "connections": {
            "default": "postgres://postgres:P@ssw0rd7@localhost:5432/postgres?charset=utf8mb4"
            },
        "apps": {
            "models": {
                "models": ["app.models", "aerich.models"],
                "default_connection": "default",
            },
        }
    }

class PostgresConnector:
    
    async def connect(self):
        await Tortoise.init(
        db_url='postgres://postgres:P@ssw0rd7@localhost:5432/postgres',
        modules={'models': ['app.models']},
        generate_schemas=True,
        add_exception_handlers=True,
    )

db = PostgresConnector()
