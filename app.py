from flask import Flask, render_template
import json
from models.rps import RPS
from models.researchField import ResearchFields
from models.jobClass import JobClass
from models.software import Software

app = Flask(__name__)

@app.route("/")
def hello_world():

    rps = RPS.select()
    research_fields = ResearchFields.select().order_by(ResearchFields.field_name)
    return render_template("questions.html", 
                           rps = rps, 
                           research_fields = research_fields)

@app.route("/get_job_classes")
def get_job_classes_no_input():
    job_classes = JobClass.select().order_by(JobClass.class_name)
    return ([job.class_name for job in job_classes])

@app.route("/get_job_classes/<userInput>")
def get_job_classes_input(userInput):
    job_classes = JobClass.select().order_by(JobClass.class_name)
    filtered_job_classes = [job for job in job_classes if userInput.lower() in job.class_name.lower()]
    return ([job.class_name for job in filtered_job_classes])
    
@app.route("/get_software")
def get_software():
    softwares = Software.select().order_by(Software.software_name)
    softwares_and_versions = [f"{software.software_name} {software.version}" for software in softwares]
    return softwares_and_versions

@app.route("/get_software/<userInput>")
def get_software_input(userInput):
    softwares = Software.select().order_by(Software.software_name)
    filtered_softwares = [software for software in softwares if userInput.lower() in software.software_name.lower()]
    softwares_and_versions = [f"{software.software_name} {software.version}" for software in filtered_softwares]
    return softwares_and_versions

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)