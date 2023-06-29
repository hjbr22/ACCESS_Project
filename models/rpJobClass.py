from models import *
from models.jobClass import JobClass
from models.rps import RPS

class RpJobClass(BaseModel):
    id = PrimaryKeyField()
    rp = ForeignKeyField(RPS)
    job_class = ForeignKeyField(JobClass, backref="rps_with_JobClass")
    suitability = IntegerField(default=0)