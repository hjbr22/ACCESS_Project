from models import *
from models.software import Software
from models.rps import RPS

class RpJobClass(BaseModel):
    id = PrimaryKeyField()
    rp = ForeignKeyField(RPS)
    software = ForeignKeyField(Software, backref="software")