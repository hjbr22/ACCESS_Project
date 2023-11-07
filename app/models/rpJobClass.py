from . import *
from .jobClass import JobClass
from .rps import RPS

class RpJobClass(BaseModel):
    id = PrimaryKeyField()
    rp = ForeignKeyField(RPS)
    job_class = ForeignKeyField(JobClass, backref="rps_with_JobClass")
    suitability = IntegerField(default=0)