from models import *

class GUI(BaseModel):
    id = PrimaryKeyField()
    gui = CharField(unique = True)
