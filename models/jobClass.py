from models import *

class JobClass(BaseModel):
    id = PrimaryKeyField()
    class_name = CharField(max_length=40, unique=True)
    