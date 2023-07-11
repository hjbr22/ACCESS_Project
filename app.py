from flask import Flask, render_template, request, redirect, url_for
import json
from models.rps import RPS
from models.researchField import ResearchFields
from models.jobClass import JobClass
from models.software import Software
#from logic.form_logging import log_form_data
from logic.recommendation import get_recommendations
import logging

app = Flask(__name__)

#Initialize recommendations logger
recs_logger = logging.getLogger(__name__)

#Override default logging level
recs_logger.setLevel('INFO')

#Handler/Formatter for recommendation logs. Send to recs.log with time/name of logger/level/information
recs_handler = logging.FileHandler("query.log", mode='w')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
recs_handler.setFormatter(formatter)
recs_logger.addHandler(recs_handler)

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
    data = request.get_json()
    #log_form_data(data)
    recommendations = get_recommendations(data)
    #recs_logger.info("Recommendations: %s", recommendations)
    return json.dumps(recommendations)
    # return redirect(url_for('recommender_page',recommendations=recommendations))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)