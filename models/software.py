from models import *

class Software(BaseModel):
    id = PrimaryKeyField()
    software_name = CharField()
    version = CharField()