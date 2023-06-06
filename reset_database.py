from models import db
from models.rps import RPS
from models.jobClass import JobClass
from models.rpJobClass import RpJobClass
from models.researchField import ResearchFields
from models.rpResearchField import RpResearchField
from models.software import Software
from models.rpSoftware import RpSoftware
from models.guiName import GUI
from models.rpGUI import rpGUI
from models.temp_storage import TS
from models.rp_ts import RP_TS


db.connect()

tables = db.get_tables()
print(f"the tables: {tables}")

# delete all data and create blank tables
db.drop_tables([RPS,JobClass,RpJobClass,ResearchFields,RpResearchField,Software,RpSoftware,GUI,rpGUI])
db.create_tables([RPS,JobClass,RpJobClass,ResearchFields,RpResearchField,Software,RpSoftware,GUI,rpGUI])

rps = [
    {"name":"ACES"},
    {"name":"Anvil"},
    {"name":"Bridges-2"},
    {"name":"DARWIN"},
    {"name":"Delta"},
    {"name":"Expanse"},
    {"name":"FASTER"},
    {"name":"Jetstream2"},
    {"name":"OOKAMI"},
    {"name":"KyRIC"},
    {"name":"Rockfish"},
    {"name":"Stampede-2"},
    {"name":"RANCH"},
    {"name":"Open Science Grid"},
    {"name":"Open Storage Network"},
    ]
print("Adding RPS data")
RPS.insert_many(rps).on_conflict_replace().execute()

fields = [
    {"field_name":"Biology"},
    {"field_name":"Chemistry"},
    {"field_name":"Physics"},
    {"field_name":"Computer Science"},
    {"field_name":"Civil Engineering"},
    {"field_name":"Physics"},
    {"field_name":"Civil Engineering"},
    {"field_name":"Economics"},
    {"field_name":"Linguistics"},
    {"field_name":"History"},
    {"field_name":"Agriculture"},
    {"field_name":"Medicine"},
]
print("Adding ResearchFields data")
ResearchFields.insert_many(fields).on_conflict_replace().execute()

rpResearch = [
    {"rp": RPS.get(RPS.name == "Bridges-2"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Biology")
    },
    {"rp": RPS.get(RPS.name == "stampede-2"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Biology")
    },
    {"rp": RPS.get(RPS.name == "expanse"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Biology")
    },
    {"rp": RPS.get(RPS.name == "bridges-2"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Chemistry")
    },
    {"rp": RPS.get(RPS.name == "stampede-2"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Chemistry")
    },
    {"rp": RPS.get(RPS.name == "bridges-2"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Physics")
    },
    {"rp": RPS.get(RPS.name == "stampede-2"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Physics")
    },
    {"rp": RPS.get(RPS.name == "expanse"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Physics")
    },
    {"rp": RPS.get(RPS.name == "bridges-2"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Computer Science")
    },
    {"rp": RPS.get(RPS.name == "stampede-2"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Computer Science")
    },
    {"rp": RPS.get(RPS.name == "expanse"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Computer Science")
    },
    {"rp": RPS.get(RPS.name == "jetstream2"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Civil Engineering")
    },
    {"rp": RPS.get(RPS.name == "bridges-2"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Civil Engineering")
    },
    {"rp": RPS.get(RPS.name == "jetstream2"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Economics")
    },
    {"rp": RPS.get(RPS.name == "expanse"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Economics")
    },
    {"rp": RPS.get(RPS.name == "open science grid"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Linguistics")
    },
    {"rp": RPS.get(RPS.name == "open science grid"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "History")
    },
    {"rp": RPS.get(RPS.name == "kyric"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Agriculture")
    },
    {"rp": RPS.get(RPS.name == "anvil"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Agriculture")
    },
    {"rp": RPS.get(RPS.name == "ookami"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Medicine")
    },
    {"rp": RPS.get(RPS.name == "rockfish"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Medicine")
    },
    {"rp": RPS.get(RPS.name == "bridges-2"),
     "research_field": ResearchFields.get(ResearchFields.field_name == "Medicine")
    },
]
print("Adding RpResearchField data")
RpResearchField.insert_many(rpResearch).on_conflict_replace().execute()

jobClass = [
    {"class_name":"Data Analytics"},
    {"class_name":"Data Mining"},
    {"class_name":"NLP"},
    {"class_name":"Textual Analysis"},
    {"class_name":"Modeling and Simulation"},
    {"class_name":"Bioinformatics"},
    {"class_name":"Biophysics"},
    {"class_name":"BioChemistry"},
    {"class_name":"Fluid Dynamics"},
    {"class_name":"Image Processing"},
    {"class_name":"Machine Learning"},
    {"class_name": "Materials Science"},
    {"class_name":"Astronomic Science"},
    {"class_name":"Digital Humanities"},
    {"class_name":"Computational Chemistry"},
    {"class_name":"Genomics"},
    {"class_name":"Deep Learning"},
    {"class_name":"High Energy Physics"},
    {"class_name":"Virtual Machine"},
    {"class_name":"General"},
    {"class_name":"Parallel"},
]
print("Adding JobClass data")
JobClass.insert_many(jobClass).on_conflict_replace().execute()

#Class of jobs
jobClassAndRps = {"Data Analytics":['delta', 'bridges-2', 'darwin'],
                 "Data Mining":['darwin'],
                 "NLP":['kyric'],
                 "Textual Analysis":['delta'],
                 "Modeling and Simulation":['delta'],
                 "Bioinformatics":['kyric','expanse'],
                 "Biophysics":['kyric','expanse'],
                 "Biochemistry":['kyric','expanse'],
                 "Fluid Dynamics":['delta'],
                 "Materials Science":['expanse'], 
                 "Image Processing":['darwin'], 
                 "Machine Learning":['delta','bridges-2','darwin'],
                 "Astronomic Science":['expanse'], 
                 "Digital Humanities":[], 
                 "Computational Chemistry":['expanse'], 
                 "Genomics":[], 
                 "Deep Learning":['delta'], 
                 "High Energy Physics":['expanse'],
                 "Virtual Machine":['jetstream2'], 
                 "General":['stampede-2','darwin'], 
                 "Parallel":['stampede-2']}

rpJobClass = []
for jobClass in list(jobClassAndRps.keys()):
    for rp in jobClassAndRps[jobClass]:
        rpJobClass.append({"rp": RPS.get(RPS.name == rp),
        "job_class": JobClass.get(JobClass.class_name == jobClass)
        })
print("Adding RPJobClass data")
RpJobClass.insert_many(rpJobClass).on_conflict_replace().execute()

Gui = [
    {"gui":"OpenOnDemand"},
    {"gui":"RStudio"},
    {"gui":"JupyterLab"},
    {"gui":"Exosphere"},
    {"gui":"Horizon"},
    {"gui":"CACAO"},
    ]

print("Adding GUI data")
GUI.insert_many(Gui).on_conflict_replace().execute()

#Types of GUI's

rpGUI_together = {
    "OpenOnDemand":['bridges-2', 'expanse', 'anvil', 'aces', 'faster'],
    "RStudio":['aces'],
    "JupyterLab":['aces'],
    "Exosphere":['jetstream2'],
    "Horizon":['jetstream2'],
    "CACAO":['jetstream2']}

rpgui = []
for gui in list(rpGUI_together.keys()):
    for rp in rpGUI_together[gui]:
        rpgui.append({"rp": RPS.get(RPS.name == rp),
        "rp_gui": GUI.get(GUI.gui == gui)})

print("Adding the GUI to the RP list")
rpGUI.insert_many(rpgui).on_conflict_replace().execute()


#Temporary storage in TB

temp_s = [
        {"ts":"1"},
        {"ts":"2"},
        {"ts":"100"},
        {"ts":"1.5"},
        {"ts":"30"},
        {"ts":"10"},
        {"ts":"0"},
        {"ts":"7000"}
]

#RP Temp Storage in TB

rp_temp_s = {
    "0":['ranch','bridges-2', 'jetstream2', 'open science grid', 'open storage network'],
    "1":['aces', 'faster'],
    "1.5":['delta'],
    "2":['darwin'],
    "10":['kyric','rockfish'],
    "30":['ookami'],
    "100":['anvil'],
    "7000":['expanse']
}

rp_ts = []
for temp_s in list(rp_temp_s.keys()):
    for rp in rp_temp_s[temp_s]:
        rp_ts.append({"rp": RPS.get(RPS.name == rp),
        "ts": TS.get(TS.rp_s == temp_s)})

print("Adding the Temporary Storage")
RP_TS.insert_many(RP_TS).on_conflict_replace().execute()

#Long Term Storage in TB

db.close()
