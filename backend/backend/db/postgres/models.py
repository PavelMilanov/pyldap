from tortoise import Tortoise, fields, run_async
from tortoise.models import Model
from environs import Env
from .. import env


USER = env('POSTGRES_USER')
PASSWORD = env('POSTGRES_PASSWORD')
DB = env('POSTGRES_DB')
HOST = env('POSTGRES_HOST')

TORTOISE_ORM = {
        'connections': {
            'default': f'postgres://{USER}:{PASSWORD}@{HOST}:5432/{DB}'
            },
        'apps': {
            'models': {
                'models': ['db.postgres.models', 'aerich.models'],
                'default_connection': 'default',
            },
        }
    }


class StaticIp(Model):
    id = fields.IntField(pk=True)
    ip = fields.CharField(max_length=15, unique=True)
    description = fields.TextField(null=True)

    class Meta:
        table = 'static_ip'

    def __str__(self):
        return self.ip


class Act(Model):
    id = fields.UUIDField(pk=True)
    file_name = fields.TextField()
    customer: fields.ReverseRelation['Customer']
    
    class Meta:
        table = 'acts'
    
    def __str__(self):
        return self.file_name


class Customer(Model):
    name = fields.CharField(max_length=15, pk=True)
    act = fields.ForeignKeyField('models.Act', related_name='customer', null=True)
    
    class Meta:
        table = 'customers'
        
    def __str__(self):
        return self.name
