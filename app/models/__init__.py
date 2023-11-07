from peewee import *
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR,'sqlite_db.db')
db = SqliteDatabase(db_path)

class BaseModel(Model):
    class Meta:
        database = db