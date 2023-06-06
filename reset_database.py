from models import db
from models.rps import RPS
from models.jobClass import JobClass
from models.rpJobClass import RpJobClass
from models.researchField import ResearchFields
from models.rpResearchField import RpResearchField
from models.software import Software
from models.rpSoftware import RpSoftware
from models.rp_with_GUI import GUI
from parse_modules import get_modules_and_versions

db.connect()

tables = db.get_tables()
print(f"the tables: {tables}")

# delete all data and create blank tables
db.drop_tables([RPS,JobClass,RpJobClass,ResearchFields,RpResearchField,Software,RpSoftware])
db.create_tables([RPS,JobClass,RpJobClass,ResearchFields,RpResearchField,Software,RpSoftware])

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

# rp_with_GUI = [
#     {"GUI":"ACES"},
#     {"GUI": "Anvil"},
#     {"GUI": "Bridges-2"},
#     {"GUI": "Delta"},
#     {"GUI": "Expanse"},
#     {"GUI": "FASTER"},
#     {"GUI": "Jetstream2"},
#     {"GUI": "Stampede-2"}]

# print("Adding GUI data")
# GUI.insert_many(rp_with_GUI).on_conflict_replace().execute()

# stampede modules
stampedeFile = "stampede_available_modules.txt"

stampedeModules = get_modules_and_versions(stampedeFile)
# add modules to db
software = []
for mod in stampedeModules:
    software.append({"software_name":mod[0],
                        "version":mod[1]})
    
print("Adding Software")
Software.insert_many(software).on_conflict_replace().execute()

# associate modules with stampede
stampede_mod = []
for mod in stampedeModules:
    stampede_mod.append({"rp":RPS.get(RPS.name=="Stampede-2"),
                        "software": Software.get(Software.software_name==mod[0], Software.version==mod[1])})
print("Associating Stampede and software")
RpSoftware.insert_many(stampede_mod).on_conflict_replace().execute()
db.close()
