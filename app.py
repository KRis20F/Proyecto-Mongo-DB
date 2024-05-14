import bd
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    data = request.form
    neighborhood = data["neighborhood"]
    is_created = bd.search_results(neighborhood, int(data["date"]))

    if is_created:
        return render_template("result.html", neighborhood=neighborhood, is_created=is_created)
    else:
        return render_template("index.html")


app.run(host='localhost', port=5069, debug=True)