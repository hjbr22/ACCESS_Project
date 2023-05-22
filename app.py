from flask import Flask, render_template
from models import db
from models.rps import RPS
from models.jobClass import JobClass
from models.rpJobClass import RpJobClass
from models.researchField import ResearchFields
from models.rpResearchField import RpResearchField

app = Flask(__name__)

# example of how to add things to the database
db.connect()

tables = db.get_tables()
print(f"the tables: {tables}")

db.drop_tables([RPS,JobClass,RpJobClass,ResearchFields,RpResearchField])

db.create_tables([RPS,JobClass,RpJobClass,ResearchFields, RpResearchField])

rp1 = RPS.get_or_create(name='aces')
rp2 = RPS.get_or_create(name='bridges')

job_class = JobClass.get_or_create(class_name="Biology")


rpJob = RpJobClass.get_or_create(rp=RPS.select().where(RPS.name == 'bridges'),job_class=JobClass.get_by_id(1))
# print(rpJob[0].id)
print(f"prining rpJob, rp: {rpJob[0].rp.name}, job: {rpJob[0].job_class.class_name}")
db.close()


@app.route("/")
def hello_world():
    return render_template("questions.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)