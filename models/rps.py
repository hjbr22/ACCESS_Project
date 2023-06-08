from models import *

class RPS(BaseModel):
    id = PrimaryKeyField()
    name = CharField(unique=True, constraints=[SQL('COLLATE NOCASE')])
    parallel = BooleanField(default=False)
    