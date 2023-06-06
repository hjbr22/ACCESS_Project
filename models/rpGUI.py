from models import *
from models.guiName import GUI
from models.rps import RPS

class rpGUI(BaseModel):
    id = PrimaryKeyField()
    rp = ForeignKeyField(RPS)
    rp_gui = ForeignKeyField(GUI, backref="rp_with_GUI")
