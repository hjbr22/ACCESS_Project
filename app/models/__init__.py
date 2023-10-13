from peewee import *

db = SqliteDatabase("./sqlite_db.db")

class BaseModel(Model):
    class Meta:
        database = db