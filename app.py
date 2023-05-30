from flask import Flask, render_template
from models.rps import RPS
from models.researchField import ResearchFields

app = Flask(__name__)


@app.route("/")
def hello_world():

    rps = RPS.select()
    research_fields = ResearchFields.select().order_by(ResearchFields.field_name)
    return render_template("questions.html", 
                           rps = rps, 
                           research_fields = research_fields)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)