from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
import matplotlib.pyplot as plt
import requests
                                                                                                                                       
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

@app.route('/paris/')
def meteo():
    response = urlopen('https://api.openweathermap.org/data/2.5/forecast/daily?q=Paris,fr&cnt=16&appid=bd5e378503939ddaee76f12ad7a97608')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('temp', {}).get('day') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)
  
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})

# Route pour afficher le graphique des commits par minute
@app.route('/commits/')
def commits_graph():
    # Requête à l'API GitHub pour obtenir les commits
    response = requests.get('https://api.github.com/repos/eliott194/5MCSI_Metriques/commits')
    commits = response.json()

    
    commit_minutes = [datetime.strptime(commit['commit']['author']['date'], '%Y-%m-%dT%H:%M:%SZ').minute for commit in commits]

    
    minutes_count = {}
    for minute in commit_minutes:
        if minute in minutes_count:
            minutes_count[minute] += 1
        else:
            minutes_count[minute] = 1

    # Création d'un graphique
    plt.figure(figsize=(10, 6))
    plt.bar(minutes_count.keys(), minutes_count.values(), color='blue')
    plt.xlabel('Minutes')
    plt.ylabel('Nombre de commits')
    plt.title('Commits par minute')
    plt.savefig('commits_by_minute.png')
    
    return '<img src="commits_by_minute.png" />'


  
if __name__ == "__main__":
  app.debug = True
  app.run(debug=True)
  
