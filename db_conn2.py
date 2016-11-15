from peewee import *


database = MySQLDatabase('mobei3', **{'port': 3306, 'host': '192.168.10.127', 'user': 'wcj', 'password': 'something'})

class BaseModel(Model):
    class Meta:
            database = database

class Version(BaseModel):
    version = IntegerField()

    class Meta:
        db_table = 'version'

class File(BaseModel):
    add_time = BigIntegerField()
    analysistime = BigIntegerField()
    buildirtime = BigIntegerField()
    decompiletime = BigIntegerField()
    filepath = CharField()
    finishedtime = BigIntegerField()
    formatime = BigIntegerField()
    md5 = CharField()
    sha256 = CharField()
    status = IntegerField()
    unziptime = BigIntegerField()
    updatetime = BigIntegerField()
    version = ForeignKeyField(db_column='version', rel_model=Version, to_field='id')

    class Meta:
        db_table = 'file'
        indexes = (
            (('md5', 'sha256'), True),
        )

class ErrorMessage(BaseModel):
    add_time = BigIntegerField()
    crash_flag = IntegerField()
    error_location = CharField()
    error_message = CharField()
    error_type = IntegerField()
    file = ForeignKeyField(db_column='file_id', rel_model=File, to_field='id')

    class Meta:
        db_table = 'error_message'

class ErrorTask(BaseModel):
    add_time = BigIntegerField()
    error_message = CharField()
    task = CharField(db_column='task_id')

    class Meta:
        db_table = 'error_task'

class Result(BaseModel):
    add_time = BigIntegerField()
    file = ForeignKeyField(db_column='file_id', rel_model=File, to_field='id')
    result = TextField()

    class Meta:
        db_table = 'result'

class TaskidFile(BaseModel):
    add_time = BigIntegerField()
    file = ForeignKeyField(db_column='file_id', rel_model=File, to_field='id')
    scan_app_url = TextField()
    task = CharField(db_column='task_id', unique=True)
    update_time = BigIntegerField()
    worker = CharField(db_column='worker_id')

    class Meta:
        db_table = 'taskid_file'