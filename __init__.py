from flask import Flask, render_template, jsonify
import json
from datetime import datetime
from urllib.request import urlopen

app = Flask(__name__)

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")

@app.route("/commits/")
def moncommits():
    try:
        response = urlopen('https://api.github.com/repos/eliott194/5MCSI_Metriques/commits')
        raw_content = response.read()
        json_content = json.loads(raw_content.decode('utf-8'))
        results = []
        for commit in json_content:
            commit_date = commit['commit']['author']['date']
            commit_author = commit['commit']['author']['name']  
            commit_commit = commit['sha']
            results.append({
                'date': commit_date,
                'author': commit_author,
                'commit': commit_commit
            })
        return jsonify(results=results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/com/")
def moncom():
    return render_template("commits.html")

@app.route('/paris/')
def meteo():
    try:
        response = urlopen('https://api.openweathermap.org/data/2.5/forecast/daily?q=Paris,fr&cnt=16&appid=YOUR_API_KEY')
        raw_content = response.read()
        json_content = json.loads(raw_content.decode('utf-8'))
        results = []
        for list_element in json_content.get('list', []):
            dt_value = list_element.get('dt')
            temp_day_value = list_element.get('temp', {}).get('day', 0) - 273.15
            results.append({'Jour': dt_value, 'temp': temp_day_value})
        return jsonify(results=results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def hello_world():
    return render_template('hello.html')

if __name__ == "__main__":
    app.run(debug=True)
