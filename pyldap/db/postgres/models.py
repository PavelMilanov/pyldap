from tortoise import Tortoise, fields, run_async
from tortoise.models import Model


TORTOISE_ORM = {
        "connections": {
            "default": "postgres://local:P@ssw0rd7@localhost:5432/local"
            },
        "apps": {
            "models": {
                "models": ["db.postgres.models", "aerich.models"],
                "default_connection": "default",
            },
        }
    }



class StaicIp(Model):
    ip = fields.CharField(pk=True, max_length=15)
    description = fields.TextField(null=True)

    class Meta:
        table = "static_ip"

    def __str__(self):
        return self.ip