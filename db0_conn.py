from peewee import *

database = MySQLDatabase('mobei4', **{'user': 'wcj', 'password': 'something', 'host': '192.168.10.129', 'port': 3306})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Worker(BaseModel):
    ip = CharField(unique=True)

    class Meta:
        db_table = 'worker'

class TaskidWorker(BaseModel):
    add_time = BigIntegerField(null=True)
    scan_app_url = TextField()
    task = CharField(db_column='task_id', unique=True)
    updatetime = BigIntegerField(null=True)
    worker = ForeignKeyField(db_column='worker_id', rel_model=Worker, to_field='id')

    class Meta:
        db_table = 'taskid_worker'

