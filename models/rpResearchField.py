from models import *
from models.rps import RPS
from models.researchField import ResearchFields

class RpResearchField(BaseModel):
    id = PrimaryKeyField()
    rp = ForeignKeyField(RPS)
    research_field = ForeignKeyField(ResearchFields, backref='rp_with_ResearchField')