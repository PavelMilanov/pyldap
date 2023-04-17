from tortoise import Tortoise
from tortoise import Tortoise, fields, run_async
from tortoise.models import Model


TORTOISE_ORM = {
        "connections": {
            "default": "postgres://postgres:P@ssw0rd7@localhost:5432/postgres?charset=utf8mb4"
            },
        "apps": {
            "models": {
                "models": ["db.postgres", "aerich.models"],
                "default_connection": "default",
            },
        }
    }



class Event(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    datetime = fields.DatetimeField(null=True)

    class Meta:
        table = "event"

    def __str__(self):
        return self.name