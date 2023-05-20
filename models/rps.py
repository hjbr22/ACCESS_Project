from models import *

class RPS(BaseModel):
    id = PrimaryKeyField()
    name = CharField(unique=True)
    