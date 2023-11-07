from . import *
from .rps import RPS
class RpInfo(BaseModel):
    id = PrimaryKeyField()
    rp = ForeignKeyField(RPS)
    blurb = TextField()
    link = CharField(max_length=300)
    documentation = CharField(max_length=300)