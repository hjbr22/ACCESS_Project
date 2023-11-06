from . import *
from .rps import RPS
from .researchField import ResearchFields

class RpResearchField(BaseModel):
    id = PrimaryKeyField()
    rp = ForeignKeyField(RPS)
    research_field = ForeignKeyField(ResearchFields, backref='rp_with_ResearchField')
    suitability = IntegerField(default=0)