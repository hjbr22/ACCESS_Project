from models import *
from models.gui import GUI
from models.rps import RPS

class RpGUI(BaseModel):
    id = PrimaryKeyField()
    rp = ForeignKeyField(RPS)
    gui = ForeignKeyField(GUI, backref="rp_with_GUI")
