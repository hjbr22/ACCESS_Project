from . import *

class GUI(BaseModel):
    id = PrimaryKeyField()
    gui_name = CharField(max_length=40, unique=True, constraints=[SQL('COLLATE NOCASE')])
