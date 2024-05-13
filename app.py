import db
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result")
def result():
    info = {}

    data = request.form
    info["neighborhood"] = data["neighborhood"]
    info["date"] = data["date"]
    
    is_created = db.search_result(info)

    if is_created:
        return render_template("result.html")
    else:
        return render_template("index.html")

app.run(host='localhost', port=5069, debug=True)