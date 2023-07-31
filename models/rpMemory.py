from models import *
from models.rps import RPS

class RpMemory(BaseModel):
    id = PrimaryKeyField()
    rp = ForeignKeyField(RPS)
    node_type = CharField(max_length=40)
    per_node_memory = IntegerField(default=0)