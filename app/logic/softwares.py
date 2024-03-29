from models.rps import RPS
from models.rpSoftware import RpSoftware

def get_softwares(rpName):
    rp = RPS.select().where(RPS.name==rpName)
    softwares = RpSoftware.select().where(RpSoftware.rp == rp).order_by(RpSoftware.rp.name)
    return(softwares)