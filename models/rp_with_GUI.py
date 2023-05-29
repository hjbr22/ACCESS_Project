from models import *

class GUI(BaseModel):
    id = PrimaryKeyField()
    gui = CharField(max_length=40)
