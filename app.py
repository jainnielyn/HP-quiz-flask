from flask import Flask, request, render_template, url_for
import requests, json
import random
import config

app = Flask(__name__)

# Get all spells from API
response = requests.get(f"https://www.potterapi.com/v1/spells?key={config.api_key}")
spells = response.json()
# Global variable for a list of dict with question, multiple choice, and answer
test_list = []


def get_questions(num):
    # Get num amount of spell questions, and multiple choice options
    test_spells = random.sample(spells, num)
    options = spells
    options = [o['spell'] for o in options]

    # Accessing global variable
    global test_list

    for s in test_spells:
        answer = s['spell'] # what if answer in o
        o = random.sample(options,3) 
        o.append(answer)
        random.shuffle(o)
        test_list.append({'spell':s['spell'], 'type':s['type'], 'effect':s['effect'], 'options':o})
    return test_list


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        # User input number of questions
        num = int(request.form['num'])

        # Get questions from API
        test_list = get_questions(num)
        ##
        print(test_list)

        # Display test
        return render_template("index.html", test_list=test_list)
    else:
        return render_template("index.html")


@app.route('/quiz', methods=['POST'])
def quiz():
    correct = 0

    try:
        for i in range(len(test_list)):
            answered = request.form[str(i)+'options']
            if answered == test_list[i]['spell']:
                correct += 1
    
    except:
        pass

    return render_template("result.html", correct=correct)


@app.route('/replay', methods=['POST'])
def replay():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)