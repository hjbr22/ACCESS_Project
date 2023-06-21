from flask import Flask, render_template, request, redirect, url_for
import json
from models.rps import RPS
from models.researchField import ResearchFields
from models.jobClass import JobClass
from models.software import Software
from logic.recommendation import get_recommendations

app = Flask(__name__)

@app.route("/")
def recommender_page():

    rps = RPS.select()
    research_fields = ResearchFields.select().order_by(ResearchFields.field_name)
    return render_template("questions.html", 
                           rps = rps, 
                           research_fields = research_fields)

@app.route("/get_job_classes")
def get_job_classes():
    job_classes = JobClass.select().order_by(JobClass.class_name)
    return([job.class_name for job in job_classes])
    
@app.route("/get_software")
def get_software():
    softwares = Software.select().order_by(Software.software_name)
    softwares_and_versions = [f"{software.software_name}" for software in softwares]

    return softwares_and_versions

@app.route("/get_score", methods=['POST'])
def get_score():
    print("hello")
    data = request.get_json()
    print(data)
    print(f"software data: {data['software']}, software data length: {len(data['software'])}, does it exist: {bool(data['software'])}")
    recommendations = get_recommendations(data)
    print(recommendations)
    return json.dumps(recommendations)
    # return redirect(url_for('recommender_page',recommendations=recommendations))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)