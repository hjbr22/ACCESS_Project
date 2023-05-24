from models import db
from models.rps import RPS
from models.jobClass import JobClass
from models.rpJobClass import RpJobClass
from models.researchField import ResearchFields
from models.rpResearchField import RpResearchField
from models.software import Software
from models.rpSoftware import RpSoftware


# example of how to add things to the database
db.connect()

tables = db.get_tables()
print(f"the tables: {tables}")

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
RPS.insert_many(rps).on_conflict_replace().execute()

jobClass = [
    {"class_name":"Biology"},
    {"class_name":"Chemistry"},
    {"class_name":"Physics"},
    {"class_name":"Computer Science"},
    {"class_name":"Civil Engineering"},
    {"class_name":"Physics"},
    {"class_name":"Civil Engineering"},
    {"class_name":"Economics"},
    {"class_name":"Linguistics"},
    {"class_name":"History"},
    {"class_name":"Agriculture"},
    {"class_name":"Medicine"},
]
JobClass.insert_many(jobClass).on_conflict_replace().execute()

{"Biology":['bridges','stampede','expanse'], 
                "Chemistry":['bridges','stampede'], 
                "Physics":['bridges','stampede','expanse'], 
                "Computer Science":['bridges','stampede','expanse'], 
                "Civil Engineering":['jetstream','bridges'], 
                "Economics":['jetstream','expanse'],
                "Linguistics":['osg'], 
                "History":['osg'], 
                "Agriculture":['kyric','anvil'], 
                "Medicine":['ookami','rockfish','bridges']}

job_class = JobClass.get_or_create(class_name="Biology")


rpJob = RpJobClass.get_or_create(rp=RPS.select().where(RPS.name == 'bridges'),job_class=JobClass.get_by_id(1))
# print(rpJob[0].id)
print(f"prining rpJob, rp: {rpJob[0].rp.name}, job: {rpJob[0].job_class.class_name}")
db.close()
