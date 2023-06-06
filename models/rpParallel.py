from models import *
from models.rps import RPS

class RpParallel(BaseModel):
    id = PrimaryKeyField()
    rp = ForeignKeyField(RPS)
    rp_parallel = BooleanField(default=False)