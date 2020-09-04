from flask import Flask, request, render_template, url_for
import requests, json
import random
import config

app = Flask(__name__)

def get_questions(num):
    # Get all spells from API
    response = requests.get(f"https://www.potterapi.com/v1/spells?key={config.api_key}")
    spells = response.json()

    # Get num amount of spell questions, and multiple choice options
    test_spells = random.sample(spells, num)
    options = random.sample(spells, num*3)
    options = [o['spell'] for o in options]

    # Create a list of dictionaries where each dict has Q, A and options
    test_list = []

    for s in test_spells:
        answer = s['spell'] # what if answer in o
        o = random.sample(options,3) # add answer and randomize
        test_list.append({'spell':s['spell'], 'type':s['type'], 'effect'['effect'], 'options':o})
    return test_list

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        # User input number of questions
        num = int(request.form['num'])

        # Get questions from API
        test_spells, options = get_questions(num)
        print(test_spells)

        # Display test
        return render_template("index.html", test_list=test_list)
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)