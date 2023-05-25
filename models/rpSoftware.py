from models import *
from models.software import Software
from models.rps import RPS

class RpSoftware(BaseModel):
    id = PrimaryKeyField()
    rp = ForeignKeyField(RPS)
    software = ForeignKeyField(Software, backref="rp_with_Software")