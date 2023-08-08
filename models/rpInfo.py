from models import *
from models.rps import RPS
class RpInfo(BaseModel):
    id = PrimaryKeyField()
    rp = ForeignKeyField(RPS)
    blurb = TextField()
    link = CharField(max_length=300)