from models.rps import RPS
from models.software import Software

def organize_modules(parsed, rp_id):
    #Takes the filename and inputs that data into the specific RP that it is associated with
    #Need the rps file in order to associate the given RP
        #Go through the file and add all of the softwares
    rp_modules = []
    for line in parsed:
        rp_modules.append({"rp":RPS.get(RPS.name == rp_id), 
                            "software":Software.get(Software.software_name == line[0], Software.version == line[1]), 
                           "suitability":1})
    return(rp_modules)
