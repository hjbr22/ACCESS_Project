from . import *

class ResearchFields(BaseModel):
    id = PrimaryKeyField()
    field_name = CharField(max_length=40, unique=True)
