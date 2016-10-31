from peewee import *


database2 = MySQLDatabase('mobei3', **{'port': 3306, 'host': '192.168.230.128', 'user': 'root', 'password': 'root'})

class BaseModel(Model):
    class Meta:
            database = database2

class Version(BaseModel):
    version = IntegerField()

    class Meta:
        db_table = 'version'

class File(BaseModel):
    filepath = CharField()
    md5 = CharField()
    sha256 = CharField()
    status = IntegerField()
    updatetime = BigIntegerField()
    version = ForeignKeyField(db_column='version', rel_model=Version, to_field='id')

    class Meta:
        db_table = 'file'
        indexes = (
            (('md5', 'sha256'), True),
        )

class ErrorMessage(BaseModel):
    crash_flag = IntegerField()
    error_location = CharField()
    error_message = CharField()
    error_type = IntegerField()
    file = ForeignKeyField(db_column='file_id', rel_model=File, to_field='id')

    class Meta:
        db_table = 'error_message'

class Result(BaseModel):
    file = ForeignKeyField(db_column='file_id', rel_model=File, to_field='id')
    result = TextField()

    class Meta:
        db_table = 'result'

class TaskidFile(BaseModel):
    file = ForeignKeyField(db_column='file_id', rel_model=File, to_field='id')
    scan_app_url = TextField()
    task = CharField(db_column='task_id', unique=True)

    class Meta:
        db_table = 'taskid_file'