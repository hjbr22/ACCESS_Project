from models import *

class RPS(BaseModel):
    id = PrimaryKeyField()
    name = CharField(unique=True, constraints=[SQL('COLLATE NOCASE')])
    scratch_tb = FloatField()
    longterm_tb = FloatField()
    parallel = IntegerField(default=0)