from flask import Flask, render_template
from models.rps import RPS

app = Flask(__name__)


@app.route("/")
def hello_world():

    rps = RPS.select()
    print(rps)
    for rp in rps:
        print(rp.name)
    return render_template("questions.html", rps = rps)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)